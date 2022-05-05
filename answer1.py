def server_disorder_output(logfile):
  with open(logfile, 'r') as f:
    #それぞれのサーバーに対して、状態のリストを収納した辞書dic_serversを作成。（キー：サーバー名、値（＝状態）：[[時間,応答時間], [時間,応答時間], ...]）
    dic_servers = {}
    for eachlog in f:
      eachlog = eachlog.split(',')
      eachlog[2] = eachlog[2].replace('\n', '')
      if eachlog[1] not in dic_servers.keys():
        dic_servers[eachlog[1]] = [[eachlog[0], eachlog[2]]]
      else:
        dic_servers[eachlog[1]].append([eachlog[0], eachlog[2]])

    #各々のサーバーに対して、もしタイムアウトしていたならその始点と終点をsince_time,until_timeとして出力。タイムアウトしていないなら何もしない
    for server, condition in dic_servers.items():
      since_time_list = []
      for i, each_condition in enumerate(condition):
      #もしタイムアウトがその任意のリストにあり、直前のリストにないなら（＝そこでタイムアウトが「発生」したなら）
        if '-' in each_condition[1] and (i == 0 or (i >= 1 and '-' not in condition[i-1][1])):
          since_time_list.append(each_condition[0])
          since_time = min(since_time_list)
          while i+1 < len(condition)  and '-' in condition[i+1][1]: #次に応答するときのインデックスを発見、応答していない場合until_timeにnowを表示
            i += 1
            print(i)
            if i+1 == len(condition):
              until_time = "now"
            else:
              until_time = condition[i+1][0]
          with open('output1.txt', 'a') as o:
              print('SERVER ERROR: server_name: "'+server+'" since '+since_time+' until '+until_time, file=o)
