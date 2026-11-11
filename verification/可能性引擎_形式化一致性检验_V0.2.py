"""Possibility Engine formal consistency check V0.2.

Replays the 13 bounded propositional cases from V0.1, then runs five
clarification tests for V0.2's 'public registry != unrestricted access' rule.

This is a *bounded propositional* test, not a complete modal/deontic proof.
"""
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from sympy import And, Not, Implies

origin = Path(__file__).with_name('可能性引擎_形式化一致性检验_V0.1.py')
spec = spec_from_file_location('possibility_v01', origin)
old = module_from_spec(spec)
spec.loader.exec_module(old)
var, case, CASES = old.var, old.case, old.CASES

# 14: A registered historical source can be publicly discoverable even
# if a particular member of the public has no permission to read its text.
registered, discoverable, research_path, auth_1, auth_2, read_1, read_2 = var(
    'registered discoverable research_path auth_1 auth_2 read_1 read_2')
case('登记与任意访问的分离', 'SAT', [
    ('纳入公共知识体系', registered),
    ('可被发现', discoverable),
    ('至少存在合规研究通道', research_path),
    ('研究者甲有权限', auth_1), ('研究者甲可读取', read_1),
    ('研究者乙无权限', Not(auth_2)), ('研究者乙不可读取', Not(read_2)),
    ('读取必须获得授权', And(Implies(read_1, auth_1), Implies(read_2, auth_2))),
    ('登记要求具备研究路径', Implies(registered, research_path))
], 'V0.2：最终公开/登记不推出每个主体均可无条件阅读。')

# 15: Registration can happen despite a risk that persists during
# every step of the *finite model*; text access remains controlled.
risk0, risk1, risk2, register2, controlled2, unrestricted2, protected = var(
    'risk0 risk1 risk2 register2 controlled2 unrestricted2 protected')
case('风险持续时依然登记并实施分级访问', 'SAT', [
    ('有限窗口内风险一直存在', And(risk0, risk1, risk2)),
    ('末期完成知识体系登记', register2),
    ('末期依然采取授权访问', controlled2),
    ('没有无条件全文访问', Not(unrestricted2)),
    ('保留适当防护', protected),
], 'V0.2：风险与公共可追索性可以并存，但尚不证明无限未来的实际安全。')

# 16: Facts about history alone do not entail a specific institutional duty.
historical_event, factual_record, registered_now, registered_later = var(
    'historical_event factual_record registered_now registered_later')
case('事实前提不能单独推出最终公开规范', 'SAT', [
    ('历史事件确实发生', historical_event), ('有关记录存在', factual_record),
    ('此有限模型当下未登记', Not(registered_now)),
    ('有限模型下一时点仍未登记', Not(registered_later)),
], '反模型见证：从纯事实命题无法逻辑推出另设的规范公理；不是对该公理的否定。')

# 17: Empty nominal publicity violates V0.2's stronger notion of registration.
empty_registered, valid_study_path = var('empty_registered valid_study_path')
case('名义公开但无任何研究通道（违反定义）', 'UNSAT', [
    ('记录被标记为公开', empty_registered),
    ('不存在任何合法有效研究路径', Not(valid_study_path)),
    ('V0.2公开定义：登记须可追索且有实际研究路径',
     Implies(empty_registered, valid_study_path)),
], '否定测试：纯名义登记不足以履行V0.2公开原则。')

# 18: A history-preservation obligation can be satisfied by an authorized
# custodian even when the individual engine is forbidden to hold the copy.
exists, local_ban, local_hold, custodian_hold, provenance, access_control = var(
    'exists local_ban local_hold custodian_hold provenance access_control')
case('历史保全与合法第三方保管', 'SAT', [
    ('原始记录存在', exists),
    ('系统受到直接持有禁令', local_ban),
    ('系统并不直接持有', Not(local_hold)),
    ('合规保管主体保有原始记录', custodian_hold),
    ('原始来源链可追溯', provenance),
    ('访问仍受控制', access_control),
], '存在性示例：持有权限与保全目标可分离，不保证现实中总有合规保管主体。')

if __name__ == '__main__':
    sat = sum(c['status'] == 'SAT' for c in CASES)
    unsat = sum(c['status'] == 'UNSAT' for c in CASES)
    print(f'Possibility Engine V0.2 bounded proposition tests: {len(CASES)} cases, {sat} SAT, {unsat} UNSAT')
    for i, c in enumerate(CASES, 1):
        print(f'{i:02d} {c["status"]:5s} {c["name"]}')
        if c['core']:
            print('    Minimal UNSAT subset:', ' / '.join(c['core']))
