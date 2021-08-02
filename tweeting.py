import tweepy

# authv = "KdRmNduC759tyi9ypyc956L42"
# auths = 'W9rlv8lfQdQuRnO8Ns0uAHpMt5F84MQi1xtMePn3GihYFTiLk4'
# token = '1419322599440633859-3szguL4Tv4sZHBLlG3c4yljGeBWaVK'
# tokens = 'nxIPYQDKJAWvxWtBBm2uI8nAHhAbzQERSdOV8gGI8N5W5'

def uploadTwitter(pathi, thread, i, ID):
    if thread.currentIDs[i] != thread.threadID:
        authv = thread.replyauthv
        auths = thread.replyauths
        token = thread.replytoken
        tokens = thread.replytokens
    else:
        authv = thread.OPauthv
        auths = thread.OPauths
        token = thread.OPtoken
        tokens = thread.OPtokens

    auth = tweepy.OAuthHandler(authv, auths)
    auth.set_access_token(token, tokens)
    api = tweepy.API(auth)
    message = thread.MSGS[i]
    if len(message)>140:
        message = message[:139]
    if thread.currentIDs[i] != thread.threadID:
        if message != thread.MSGS[i-1]:
            replyID = thread.TwitterIDs[0]
            if len(ID) > 0:
                for i, aID in enumerate(thread.postIDs):
                    if aID == ID:
                        replyID = thread.TwitterIDs[i]
            if replyID == thread.TwitterIDs[0]:
                message = '@LafeChan'+ thread.board + ' ' + message
            else:
                message = '@ylylrepost' + ' ' + message
            if "." in pathi:
                tweet = api.update_with_media(pathi, status=message, in_reply_to_status_id = replyID)
            else:
                tweet = api.update_status(message, in_reply_to_status_id = replyID)
        else:
            thread.TwitterIDs.append(thread.TwitterIDs[i-1])
    else:
        if "." in pathi:
            tweet = api.update_with_media(pathi, status=message)
        else:
            tweet = api.update_status(message)
            print("dun goofed")
    ID = tweet.id_str
    thread.TwitterIDs.append(ID)
