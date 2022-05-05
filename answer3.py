def server_disorder_output(logfile, N, m, t):
  with open(logfile, 'r') as f:
    dic_servers = {}
    for eachlog in f:
      eachlog = eachlog.split(',')
      eachlog[2] = eachlog[2].replace('\n', '')
      if eachlog[1] not in dic_servers.keys():
        dic_servers[eachlog[1]] = [[eachlog[0], eachlog[2]]]
      else:
        dic_servers[eachlog[1]].append([eachlog[0], eachlog[2]])

    for server, condition in dic_servers.items():
      for i, each_condition in enumerate(condition):
        if '-' in each_condition[1] and (i == 0 or (i >= 1 and '-' not in condition[i-1][1])):
          j = 0
          while i+j+1 < len(condition) and '-' in condition[i+j+1][1]: 
              j += 1

          if j+1 >= N:
            since_time = each_condition[0]
            if i+j+1 == len(condition):
              until_time = "now"
            else:
              until_time = condition[i+j+1][0]

            with open('output3.txt', 'a') as o:
                  print('SERVER ERROR: server_name: "'+server+'" since '+since_time+' until '+until_time, file=o)
    
    for server, condition in dic_servers.items():
      latency_list = []

      #応答時間のみのリストlatency_listを作成する。
      for each_condition in condition:
        latency_list.append(each_condition[1])

      #latency_listを前からm個ずつのリストm_latencyに分割する。ただし重複があってもよい。
      for i in range(0,len(latency_list)-m+1):
        m_latency = latency_list[i:i+m]
      #'-'を含むリストは作らない。
        if '-' in m_latency:
          continue
      
      #m_latencyの総和sum_latencyを計算し、その平均average_latencyを計算する。
        sum_latency = 0
        for k in m_latency:
          sum_latency += int(k)
        average_latency = sum_latency/m

      #average_latencyがtより大きいものについて、since_timeとuntil_timeを出力する。
        if average_latency >= t:
          since_time = condition[i][0]
          until_time = condition[i+m-1][0]
          with open ('output3.txt', 'a') as o:
            print('SERVER OVERLOAD: sever_name: "'+server+'" since: '+since_time+' until: '+until_time, file = o)

server_disorder_output("log3.txt", 3, 3, 30) #暫定的にfilename='log3.txt',N=3, m=3, t=30としています。実行する際に書き換えてください。