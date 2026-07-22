from protocols import protocols
scores = {}
base_scores = {}
region_scores = {}
mode_scores = {}
manual_scores = {}
final_score = {}
servers_score = {}

MIN_SCORE = -200
MAX_SCORE = 200


for protocol in protocols:
    scores[protocol] = 0
    base_scores[protocol] = 0
    region_scores[protocol] = 0
    mode_scores[protocol] = 0
    manual_scores[protocol] = 0
    final_score[protocol] = 0

def clamp_score(value):
    return max(MIN_SCORE, min(MAX_SCORE, value))

def calcul_result():
    global final_score
    global base_scores 
    global region_scores 
    global mode_scores 
    global manual_scores
    global final_score
    for protocol in protocols:
        if manual_scores[protocol] <= -200:
            final_score[protocol] = -200
        else:
            total = (
                base_scores[protocol]
                + mode_scores[protocol]
                + region_scores[protocol]
                + manual_scores[protocol]
            )

            final_score[protocol] = clamp_score(total)

#для оценки:
#100  = рекомендую
#50   = скорее хорошо
#0    = неизвестно/нейтрально
#-50  = скорее плохо
#-100 = плохо
#-200 = почти исключить

# для оценки
#0   — практически не определяется
#20  — определяется редко
#40  — определяется
#60  — определяется хорошо
#80  — определяется очень хорошо
#100 — сигнатура известна