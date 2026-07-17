#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""恢复演示：模拟 wiki-agent 被 kill（current-task.json 停在 running），
再用 `python agents/wiki-agent.py --recover --loop 1` 验证恢复路径。

步骤：
1. 备份当前 current-task.json；
2. 用 StateManager 写入一个 running 状态的假任务（历史里保留真实状态）；
3. 子进程跑 wiki-agent --recover --loop 1；
4. 断言：打印了恢复信息，且当轮任务正常完成。
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'state-manager'))

from manager import StateManager  # noqa: E402


def main():
    sm = StateManager()
    ct_path = ROOT / 'state' / 'current-task.json'
    before = ct_path.read_text(encoding='utf-8') if ct_path.exists() else None
    print('步骤 1: 伪造 running 状态（模拟上次运行被 kill）')
    fake = {
        'task_id': 'wiki-killed-demo',
        'task_type': 'check',
        'status': 'running',
        'current_step': 2,
        'total_steps': 5,
        'progress': 0.4,
        'owner_agent': 'WikiAgent',
        'context': {'summary': '被 kill 的演示任务'},
    }
    assert sm.write('current-task.json', fake, 'demo-recovery'), '伪造写入失败'
    print('  current-task.json 现在 status=running')

    print('步骤 2: 运行 python agents/wiki-agent.py --recover --loop 1')
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    proc = subprocess.run(
        [sys.executable, str(ROOT / 'agents' / 'wiki-agent.py'),
         '--recover', '--loop', '1'],
        cwd=str(ROOT), env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        encoding='utf-8')
    out = proc.stdout
    print(out)

    print('步骤 3: 断言')
    assert proc.returncode == 0, f'agent 退出码非 0: {proc.returncode}'
    assert '[recover]' in out and '已从历史恢复' in out, '未打印恢复信息'
    assert 'wiki-killed-demo' in out, '恢复信息未包含被中断的 task_id'
    assert 'WikiAgent run: 1/1 task(s) completed' in out, '当轮任务未完成'
    task = sm.read('current-task.json')
    assert task.get('status') == 'completed', f'任务状态异常: {task.get("status")}'
    print(f'  OK: 恢复信息已打印，任务 {task.get("task_id")} 正常完成')
    print(f'（备注：演示前 current-task.json 内容为 {"存在" if before else "不存在"}；'
          '恢复后又被本轮正常运行覆写为 completed，属预期行为）')
    print('demo_recovery: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
