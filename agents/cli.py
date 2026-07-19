# -*- coding: utf-8 -*-
"""agent-runtime 结构化命令层（v1.3.0 Step 1）。

一个入口五个子命令，全部是对现有 Executor / Planner 的薄分发，
不复制内核逻辑：

    agent-runtime check       跑一次 check 协议（stale/断链巡检 + 生成报告）
    agent-runtime ingest <url_or_path> --title T [--domain D] [--tags a,b]
    agent-runtime wrapup      跑 wrapup 协议（会话收尾归档）
    agent-runtime status      系统状态总览（state/ + 最新检查报告）
    agent-runtime run [--loop N] [--interval S] [--recover]   旧版循环模式

兼容旧用法：裸 `agent-runtime` 或首参数以 - 开头（如 --loop 10）
等价于 run 子命令。check/ingest/wrapup/status 支持 --json 机器可读输出，
供网页控制台（v1.3.0 Step 2）与脚本调用。

退出码：0 成功，1 失败。
"""

import argparse
import io
import json
import re
import sys
from contextlib import nullcontext, redirect_stdout
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
for _d in ('agents', 'planner', 'executor', 'state_manager', 'event_bus', 'memory'):
    _p = str(BASE / _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from executor import ProtocolExecutor  # noqa: E402  # import 即完成 stdout 编码自配置

SUBCOMMANDS = ('run', 'check', 'ingest', 'wrapup', 'status')


def _normalize_argv(argv):
    """旧式调用（无子命令）映射到 run 子命令；--help 保留给顶层帮助。"""
    argv = list(argv)
    if not argv:
        return ['run']
    if argv[0] in SUBCOMMANDS or argv[0] in ('-h', '--help'):
        return argv
    return ['run'] + argv


def _latest_report():
    """最新的 check 报告（reports/check-*.md），没有则 None。"""
    reports = sorted((BASE / 'reports').glob('check-*.md'))
    return reports[-1] if reports else None


def _report_counts(path):
    """从检查报告里抠 stale_count / broken_count，抠不到返回 None。"""
    text = path.read_text(encoding='utf-8')

    def _num(key):
        m = re.search(key + r':\s*(\d+)', text)
        return int(m.group(1)) if m else None

    return {'stale_count': _num('stale_count'), 'broken_count': _num('broken_count')}


def _print_result(result, args, ok_msg, fail_msg):
    if getattr(args, 'json', False):
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif result['ok']:
        print(ok_msg)
    else:
        print(fail_msg)


def _silent_if_json(args):
    """--json 模式下吞掉协议执行日志，保证 stdout 只有 JSON。"""
    if getattr(args, 'json', False):
        return redirect_stdout(io.StringIO())
    return nullcontext()


def _cmd_run(args):
    from wiki_agent import WikiAgent
    agent = WikiAgent()
    if args.recover:
        agent.recover_if_interrupted()
    agent.run(loop=args.loop, interval=args.interval)
    return 0


def _cmd_check(args):
    from wiki_agent import WikiAgent
    agent = WikiAgent()
    with _silent_if_json(args):
        planner_status = agent.check()
    report = _latest_report()
    result = {'ok': True, 'planner': planner_status,
              'report': report.relative_to(BASE).as_posix() if report else None,
              'stale_count': None, 'broken_count': None}
    if report:
        result.update(_report_counts(report))
    _print_result(
        result, args,
        '检查完成：stale {} 页，断链 {} 条（报告 {}）'.format(
            result['stale_count'] if result['stale_count'] is not None else '?',
            result['broken_count'] if result['broken_count'] is not None else '?',
            result['report']),
        '检查失败')
    return 0


def _cmd_ingest(args):
    ex = ProtocolExecutor()
    with _silent_if_json(args):
        ok = ex.execute('ingest', inputs={
            'url_or_path': args.url_or_path,
            'title': args.title,
            'domain': args.domain,
            'tags': args.tags,
        })
    page = '知识库/{}.md'.format(args.title.replace(' ', '_'))
    result = {'ok': ok, 'title': args.title, 'page': page}
    if not ok:
        result['state'] = {str(k): v for k, v in ex.state.items()}
    _print_result(result, args,
                  'ingest OK: {}（已更新 index.md）'.format(page),
                  'ingest FAILED: {}'.format(ex.state))
    return 0 if ok else 1


def _cmd_wrapup(args):
    ex = ProtocolExecutor()
    with _silent_if_json(args):
        ok = ex.execute('wrapup')
    result = {'ok': ok, 'state': {str(k): v for k, v in ex.state.items()}}
    _print_result(result, args, 'wrapup OK: 会话已收尾归档',
                  'wrapup FAILED: {}'.format(ex.state))
    return 0 if ok else 1


def _collect_status():
    from wiki_agent import WikiAgent
    agent = WikiAgent()
    sm = agent.planner.sm
    events_file = BASE / 'event_bus' / 'history' / 'events.jsonl'
    events_persisted = 0
    if events_file.exists():
        with events_file.open(encoding='utf-8') as f:
            events_persisted = sum(1 for _ in f)
    report = _latest_report()
    result = {
        'session': sm.read('session.json'),
        'execution': sm.read('execution-status.json'),
        'planner': agent.status(),
        'events_persisted': events_persisted,
        'latest_report': report.relative_to(BASE).as_posix() if report else None,
    }
    if report:
        result['report_counts'] = _report_counts(report)
    return result


def _cmd_status(args):
    result = _collect_status()
    if getattr(args, 'json', False):
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return 0
    s = result['session'] or {}
    e = result['execution'] or {}
    p = result['planner'] or {}
    c = result.get('report_counts') or {}
    print('会话: {}（{}）'.format(s.get('session_id'), s.get('status')))
    print('累计: 任务 {} 个，会话 {} 次，当前 {}'.format(
        e.get('tasks_processed', 0), e.get('sessions_total', 0),
        e.get('status', 'unknown')))
    print('队列: {} 个待办；已落盘事件: {} 条'.format(
        p.get('queue_size'), result['events_persisted']))
    print('最新检查: {}（stale {}，断链 {}）'.format(
        result['latest_report'],
        c.get('stale_count', '?'), c.get('broken_count', '?')))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='agent-runtime', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)

    p_run = sub.add_parser('run', help='旧版循环模式（裸 agent-runtime 的默认行为）')
    p_run.add_argument('--loop', type=int, default=1,
                       help='运行轮数（默认 1），每轮入队一个 check 任务')
    p_run.add_argument('--interval', type=float, default=0,
                       help='轮间休眠秒数（默认 0）')
    p_run.add_argument('--recover', action='store_true',
                       help='启动时恢复上次被 kill 的运行')

    p_check = sub.add_parser('check', help='跑一次知识库健康检查（stale/断链 + 报告）')
    p_check.add_argument('--json', action='store_true', help='机器可读 JSON 输出')

    p_ing = sub.add_parser('ingest', help='入库一篇外部材料（URL 或本地文件）')
    p_ing.add_argument('url_or_path', help='URL 或本地文件路径')
    p_ing.add_argument('--title', required=True, help='知识页标题')
    p_ing.add_argument('--domain', default='knowledge-management',
                       help='domain 值（须在 metadata-schema 枚举内）')
    p_ing.add_argument('--tags', default='', help='逗号分隔的标签')
    p_ing.add_argument('--json', action='store_true', help='机器可读 JSON 输出')

    p_wrap = sub.add_parser('wrapup', help='会话收尾归档（hot.md/log.md/state/下次计划）')
    p_wrap.add_argument('--json', action='store_true', help='机器可读 JSON 输出')

    p_st = sub.add_parser('status', help='系统状态总览')
    p_st.add_argument('--json', action='store_true', help='机器可读 JSON 输出')

    args = parser.parse_args(
        _normalize_argv(sys.argv[1:] if argv is None else argv))
    handler = {'run': _cmd_run, 'check': _cmd_check, 'ingest': _cmd_ingest,
               'wrapup': _cmd_wrapup, 'status': _cmd_status}[args.command]
    return handler(args)


if __name__ == '__main__':
    sys.exit(main())
