# coding=utf-8
import tungsten


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()

    client = tungsten.Tungsten(keyConfig.get('Wolfram', 'WOLF_APP_ID'))
    result = client.query(requestText)
    allAnswers = result.pods
    if len(allAnswers) > 0:
        fullAnswer = ''
        for question in allAnswers[0].format['plaintext']:
            if question is not None:
                fullAnswer += question.encode('ascii', 'ignore') + '?\n'
        if len(allAnswers) > 1:
            for pod in allAnswers[1:]:
                for answer in pod.format['plaintext']:
                    if answer is not None:
                        fullAnswer += answer.encode('ascii', 'ignore') + '.\n'
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + fullAnswer)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any answers for ' +
                                              requestText.encode('utf-8'))
