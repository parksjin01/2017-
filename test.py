# -*- encoding:utf-8 -*-
import nltk
import numpy as np

def parsing(caption):
    res = []
    switch = 0
    if '\r\n\r\n' in caption:
    	caption = caption.split('\r\n\r\n')
    else:
	caption = caption.split('\n\n')
    for sentence in caption:
        tmp = ''
        for each in sentence.split('\n')[2:]:
            for char in each:
                if char == '<' or char == '[' or char == '(':
                    switch += 1
                elif (char == '>' or char == ']' or char == ')') and switch > 0:
                    switch -= 1
                if switch == 0 and char != '>' and char != ']' and char != ')':
                    tmp += char
        if tmp:
            res.append(tmp)
    return '\n` '.join(res)

def analyze(caption, perc = 10):
    if perc > 100:
        print '[-]Percentage can\'t above 100%'
    caption = parsing(caption)
    res = {'CC':[], 'CD':[], 'DT':[], 'EX':[], 'FW':[], 'IN':[], 'JJ':[], 'JJR':[], 'JJS':[], 'LS':[], 'MD':[], 'NN':[], 'NNP':[], 'NNPS':[], 'NNS':[], 'PDT':[], 'POS':[], 'PRP':[], 'RB':[], 'RBR':[], 'RBS':[], 'RP':[], 'SYM':[], 'TO':[], 'UH':[], 'VB':[], 'VBD':[], 'VBG':[], 'VBN':[], 'VBP':[], 'VBZ':[], 'WDT':[], 'WP':[], 'WP$':[], 'WRB':[]}
    question_idx = []
    question = ''
    answer = []
    token = nltk.word_tokenize(caption)
    pos = nltk.pos_tag(token)
    for i in range(len(token)):
        tmp = pos[i]
        try:
            res[tmp[1]].append(i)
        except:
            pass
    cnt = int(len(token)*(perc/100.0))
    for pos_key in res.keys():
        tmp_len = int(cnt * float(len(res[pos_key]))/len(token))
        if tmp_len > 0:
            question_idx += list(np.random.choice(res[pos_key], tmp_len))

    for i in range(len(token)):
        if i in question_idx:
	    tmp = '<input type=text name=blank></input>'
            if i<len(token)-1 and (token[i+1] == ',' or token[i+1] == '.'):
                question += tmp
                answer.append(token[i])
            elif i < len(token)-1 and 2 <= len(token[i+1]) and len(token[i+1]) < 5 and (token[i+1][0] == "'" or (token[i+1][1] == "'" and token[i+1][0] == 'n')):
                question += tmp
                answer.append(token[i])
            else:
                question += tmp+' '
                answer.append(token[i])
        else:
            if i < len(token)-1 and (token[i+1] == ',' or token[i+1] == '.'):
                question += token[i]
            elif i < len(token)-1 and 2 <= len(token[i+1]) and len(token[i+1]) < 5 and (token[i+1][0] == "'" or (token[i+1][1] == "'" and token[i+1][0] == 'n')):
                question += token[i]
            else:
                question += token[i]+' '

    return question.replace('` ', '\n'), answer

def check_answer(user, answer):
    cnt_problem = len(answer)
    correct = 0
    for idx in range(len(user)):
	print user[idx]== answer[idx]
        if user[idx].lower() == answer[idx].lower():
            print 1
            correct += 1
    return float(correct)/cnt_problem*100

print analyze('''ダルビッシュが現地時間７月３１日、レンジャースからドジャースへと移籍した。報道によれば日本人選手がウェイバーを経ずにシーズン中にトレードになるのは初めてのことだとか。期限ギリギリでの両球団の交渉締結ということで、その背景にはさまざまな思惑が渦巻いていたと予想される。地元記者らはツイッターで〆切り前の３０分以内に入ってから、まるで実況中継のように、かなり頻繁にツイートしていたようだ。

　これも報道による情報だが、今季で契約が切れるダルビッシュ側としては、レンジャースにナショナルズがストラスバーグ投手と契約した１７～２３年の７年で、総額１億７５００万ドルという巨額を求めたが拒否されたと伝えられている。ダルビッシュの他球団移籍は濃厚と見られていたが、そうした根拠があったわけだ。

　そんな情報が正しいかどうかはともかく、メジャーでの選手の評価は「金」に象徴される。レンジャースがダルビッシュを放出したと見るか、ダルビッシュがレンジャースを見限ったと捉えるかは人それぞれだが、まあメジャーとは金と契約が多くを支配し（すべてとはいわないが）、決して安住の地はない……と感じさせられる。考えてみればアメリカという国自体が、多民族国家で歴史が浅く、常に変化している、言い換えれば安住の地のない「漂流している巨大な島のような国」だから、それも無理ないことか。余談だが、ダルビッシュはレンジャースとの契約事項に、移籍先の拒否権を盛り込んでいたともいう。契約時に、移籍先の良し悪しを盛り込む。もうその時点で、レンジャースは「今から入る球団」に過ぎないのかと思わされてしまうのは、筆者の個人的感情が強すぎるだろうか。
　
　その夜、筆者はテレビでダルビッシュのレンジャースでの記者会見を見ていた。彼はいつも記者会見では質問に答えるとき、ややうつむき加減で相手の目を見ずに答える。そして話し終わると、通訳や相手記者の顔をちらっと見る。そんなクセがある。

　そしてもうひとつ。彼はあまり喜怒哀楽を表情に出さない。公式的な場所では基本的に感情を出したくないのだろう。とてもシャイだという話もある。「優勝争うチームから誘われるのは嬉しいこと」という趣旨のことを口にしたが、笑顔はなかった。もちろん、トレードで出る人間が、怒ったり喜んだりするのは良いことではない。

　ただあのときも、ダルビッシュは表情を押し殺していた。
　
　ポスティングの末にレンジャースとの交渉が決まったとき、２０１１年のオフのことだ。それまで彼は日本ハムでプレーしていたが、周囲の「メジャーに行くのだろう」という決めつけた視線に戸惑っていた。反発さえしていた。親しい関係者の話でも「彼は北海道が気に入っているし、なにより日本ハムという球団が気に入っている。それに引き替えアメリカで暮らすことに喜びを抱いていない。なによりもメジャーでプレーすることに夢や希望を彼は抱いていない」のだと。事実、彼はテレビでのインタビューなどでも「メジャーには関心がない」と言い続けていた。

　それでも、彼ほどの才能を持った選手を、メジャーも放っておくわけがない。マスコミも報道は過熱する。さらには日本ハム球団は資金力に乏しく、長年にわたってダルビッシュに年俸を支払う能力に乏しいとされていた。だから球団としても「売り時にポスティングで送り出したい」と思っているといわれていた。

　ただなによりダルビッシュの心を変えさせたのが、相手打者たちだった。彼がマウンドに立つと、まだ投げる前から相手チームの打者たちが戦意を喪失していた。

「ダルビッシュが投げる今日は勝てない」

　そんな打席の空気を肌で感じるようになった彼は、こう思ったという。

「もうメジャーに行くしかないのかな」

　気に入っている土地。気に入っているチーム。そこでプレーしたいのに、まわりがそれを許してくれない。
　ダルビッシュがレンジャースを選んだときも、自分で自分を納得させるような、そんな表情だったと記憶している。

 あれから６年。

 移籍が決まったときの彼の表情は、まるであのときと同じに見えた。ビジネスと割り切った、醒めたような表情。「望まれていくのだから」というコメントも、期せずして同じだった。

　ちなみに、このコラムが読者の目に届いているときは、もうすでにダルビッシュがドジャースでの初登板を済ませているはずだ。トレード発表のその夜に、相手ベンチに移ってユニフォームを着替えてプレーするのがアメリカ。移籍はビジネス。プレーはビジネス。

　果たしてダルビッシュの「フィールド･オブ･ドリームス」はどこにあるのだろう。
 
''', 50)