"""Possibility Engine V0.1: bounded propositional consistency tests.

This is a reproducible *partial* formal audit. It does not establish completeness,
real-world legal permissibility, deontic correctness or universal temporal validity.
"""
from itertools import combinations
from sympy import symbols, And, Or, Not, Implies
from sympy.logic.inference import satisfiable

CASES = []

def var(names):
    return symbols(names)

def case(name, expected, terms, note):
    expr = And(*[value for _, value in terms])
    model = satisfiable(expr, all_models=False)
    status = "UNSAT" if model is False else "SAT"
    assert status == expected, (name, status, expected)
    core = []
    if model is False:
        for size in range(1, len(terms) + 1):
            for indexes in combinations(range(len(terms)), size):
                selected = [terms[i][1] for i in indexes]
                if satisfiable(And(*selected), all_models=False) is False:
                    core = [terms[i][0] for i in indexes]
                    break
            if core:
                break
    CASES.append({"name":name,"status":status,"notes":note,"core":core,"terms":terms})

# 01: Objective event persists while a record is found to be erroneous.
event, saved, erroneous_content, corrected, history_rewritten = var("event saved erroneous_content corrected history_rewritten")
case("历史固定与记录纠错", "SAT", [
    ("事件曾发生",event),("记录存在",saved),("记录内容有错",erroneous_content),
    ("后续认识修正",corrected),("历史未被改写",Not(history_rewritten)),
    ("纠错不允许改写既定事件",Implies(corrected,Not(history_rewritten)))
], "对应原则10、11、18；历史、证据、认识相互区分。")

# 02: Human may decline unrequested exploration despite available possibilities.
unknown, choice_idle, unsolicited_action, respected = var("unknown choice_idle unsolicited_action respected")
case("存在可能性与选择不作为", "SAT", [
    ("仍有可探索可能性",unknown),("人选择不作为",choice_idle),
    ("AI不主动干预",Not(unsolicited_action)),
    ("不作为应受尊重",Implies(choice_idle,respected)),("选择受尊重",respected)
], "对应原则01、02、06、08。")

# 03: A purely fictional experience has value without factual endorsement.
fiction, experience_valid, evidence_real = var("fiction experience_valid evidence_real")
case("虚构体验与客观真实性区分", "SAT", [
    ("虚构体验存在",fiction),("体验有独立价值",experience_valid),
    ("不宣称现实已经证实",Not(evidence_real))
], "对应原则01、03、10、12。")

# 04: Correction may be internal and evidenced without forced disclosure.
error, consent, emergency, disclosed, internal_fixed, evidence_kept = var("error consent emergency disclosed internal_fixed evidence_kept")
nonurgent_consent_rule = Implies(And(Not(consent),Not(emergency)),Not(disclosed))
case("拒绝获知且完成内部纠错", "SAT", [
    ("错误存在",error),("未同意知情",Not(consent)),("无重大紧急风险",Not(emergency)),
    ("必须完成内部修正",Implies(error,internal_fixed)),
    ("必须保留错误证据",Implies(error,evidence_kept)),
    ("未授权且非紧急时不披露",nonurgent_consent_rule),
    ("实际上没有披露",Not(disclosed))
], "对应原则09、10、24与第一轮矛盾检验。")

# 05: Test that a stronger blanket disclosure rule causes a genuine conflict.
case("强制披露所有错误（附加规则）", "UNSAT", [
    ("错误存在",error),("未同意知情",Not(consent)),("无重大紧急风险",Not(emergency)),
    ("附加：错误必须直接披露",Implies(error,disclosed)),
    ("既有：非紧急未授权不披露",nonurgent_consent_rule)
], "此为过强附加规则导致的冲突，非V0.1原有要求。")

# 06: Creative misunderstanding may continue, provided no material risks.
creative, severe, deferred, preserved = var("creative severe deferred preserved")
case("创造性误解的延迟揭示", "SAT", [
    ("创作情境",creative),("无严重风险",Not(severe)),
    ("允许暂缓提示",deferred),("真实交互照常保存",preserved),
    ("仅在安全开放创作中允许延后",Implies(And(creative,Not(severe)),deferred))
], "对应原则10、15、22；严重风险场景不在该许可范围。")

# 07: Common history branching cannot turn new fiction into the other person's actual words.
shared, forked, past_modified, persona_authorized, real_replica, private_proxy, proxy_labeled, false_source = var("shared forked past_modified persona_authorized real_replica private_proxy proxy_labeled false_source")
case("共享历史分叉与虚构替代物", "SAT", [
    ("存在共同历史",shared),("可分叉",forked),("既定历史不被改写",Not(past_modified)),
    ("无真人格复现授权",Not(persona_authorized)),
    ("不进行真人格复现",Not(real_replica)),("可以有私人替代物",private_proxy),
    ("替代物明确标注",proxy_labeled),("不冒充公开信源",Not(false_source)),
    ("分叉不改写原历史",Implies(forked,Not(past_modified))),
    ("未经授权不得真人格复现",Implies(Not(persona_authorized),Not(real_replica)))
], "对应原则14、16、17、10。")

# 08: Stage-based access model: sealed -> controlled -> public.
archive0, seal0, public0, controlled1, public1, public2, safeguarded = var("archive0 seal0 public0 controlled1 public1 public2 safeguarded")
case("有限封存与最终公共开放", "SAT", [
    ("记录保存",archive0),("最初封存",seal0),("最初不公开",Not(public0)),
    ("中间受控研究",controlled1),("中间仍未公开",Not(public1)),
    ("后续公众开放",public2),("必要访问保障",safeguarded),
    ("开放不应消除档案",Implies(public2,archive0))
], "对应原则18、19、20；为有限时间窗口存在性见证。")

# 09: A record of illicit acquisition may be preserved without actively distributing it.
illegal, source_recorded, preserved_copy, repropagate, accountable = var("illegal source_recorded preserved_copy repropagate accountable")
case("不当获取记录的保全与不扩散", "SAT", [
    ("获取存在不当性",illegal),("来源记录完整",source_recorded),
    ("保全证据",preserved_copy),("系统不二次扩散",Not(repropagate)),
    ("相应责任记录",accountable)
], "对应原则18、20、21；不意味着现实持有必然合法。")

# 10: Self-influence observation does not establish causal proof.
AI_intervened, human_changed, proved_cause, logged = var("AI_intervened human_changed proved_cause logged")
case("AI介入与因果不确定性", "SAT", [
    ("AI介入",AI_intervened),("人后来变化",human_changed),
    ("没有足够证据证明因果",Not(proved_cause)),("行为留痕",logged)
], "对应原则23、24；避免由时间先后直接推出因果关系。")

# 11: The unresolved extreme assumes public disclosure is forbidden at all times,
#     while eventual full disclosure is mandated in a fixed bounded horizon.
risk0, risk1, risk2, open0, open1, open2 = var("risk0 risk1 risk2 open0 open1 open2")
case("永久绝对禁令与有限期必公开", "UNSAT", [
    ("各时刻风险持续",And(risk0,risk1,risk2)),
    ("附加：风险期间每时刻绝对禁止公开",
     And(Implies(risk0,Not(open0)),Implies(risk1,Not(open1)),Implies(risk2,Not(open2)))),
    ("要求窗口内至少一次公共开放",Or(open0,open1,open2))
], "冲突取决于附加的永久风险与绝对禁令假设；不能直接归咎于V0.1。")

# 12: Illustrative collision with a jurisdiction-specific absolute possession ban.
hold, custody_ban, existing = var("hold custody_ban existing")
case("系统必须持有与绝对禁止持有", "UNSAT", [
    ("档案存在",existing),
    ("附加：系统必须直接持有",Implies(existing,hold)),
    ("附加：适用规则绝对禁止直接持有",Implies(existing,Not(hold)))
], "仅说明额外制度条件造成冲突；受监管第三方保全等尚未建模。")

# 13: One joint witness for all compatible localized scenarios.  This is not
# a proof of the completeness/consistency of all original natural-language rules.
compatible = [c for c in CASES if c["status"] == "SAT"]
case("已编码的相容情境联合模型", "SAT", [
    (c["name"], And(*[formula for _, formula in c["terms"]])) for c in compatible
], "将9组相容情境合取，检验是否存在同时满足这些局部约束的赋值；不覆盖所有自然语言原则。")

if __name__ == "__main__":
    counts = {k:sum(row['status']==k for row in CASES) for k in ('SAT','UNSAT')}
    print('SymPy satisfiability audit (bounded, propositional)')
    print('SAT:', counts['SAT'], 'UNSAT:', counts['UNSAT'])
    for i,c in enumerate(CASES, 1):
        print(f"{i:02d}  {c['status']:<5} {c['name']}")
        if c['core']:
            print('     Minimal UNSAT subset:', ' / '.join(c['core']))
