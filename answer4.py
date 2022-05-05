import ipaddress

def network_dict(server, servers_net_host):
  server = ipaddress.ip_interface(server)
  network = server.network
  if network not in servers_net_host.keys():
    servers_net_host[network] = [server]
  else:
    servers_net_host[network].append(server)

  return servers_net_host



def subnet_disorder_output(logfile, N):
  with open(logfile, 'r') as f:
    dic_servers = {}
    for eachlog in f:
      eachlog = eachlog.split(',')
      #サーバーの時間と状態を収納した辞書dic_servers。キー：サーバー名、値：[[時間,状態], [時間,状態], ...]
      if eachlog[1] not in dic_servers.keys():
        dic_servers[eachlog[1]] = [[eachlog[0], eachlog[2]]]
      else:
        dic_servers[eachlog[1]].append([eachlog[0], eachlog[2]])

    servers_ooo = {}


    #全てのサーバーについて、キー：ネットワーク部、値：サーバーアドレスとする辞書all_serversを出力
    all_server_adress = dic_servers.keys()
    all_servers = {}
    for server_adress in all_server_adress:
      all_servers = network_dict(server_adress, all_servers)

    for server, condition in dic_servers.items():
      since_time_list = []
      until_time_list = []
      for i, each_condition in enumerate(condition):
      #もしタイムアウトがその任意のリストにあり、直前のリストにないなら（＝そこでタイムアウトが「発生」したなら）
        if '-' in each_condition[1] and (i == 0 or (i >= 1 and '-' not in condition[i-1][1])):
        #次に応答するまで何回連続でタイムアウトしたかを調べる（j+1回）
          j = 0
          while i+j+1 < len(condition) and '-' in condition[i+j+1][1]: 
              j += 1

          if j+1 >= N:#もしN回以上連続なら、since_timeとuntil_timeを定義
            since_time_list.append(each_condition[0])
            if i+j+1 == len(condition):
              until_time = "now"
            else:
              until_time_list.append(condition[i+j+1][0])
              until_time = max(until_time_list)

            
            #故障しているサーバーについて、キー：ネットワーク部、値：サーバーアドレスとする辞書servers_oooを出力
            servers_ooo = network_dict(server, servers_ooo)

            #servers_oooのキーと同じall_serversのキーについて、値（ネットワークアドレス）がすべて同じならば、サブネットがダウンしていると判定し、サーバー名とsince_time, until_timeを出力
            for keys_network in servers_ooo.keys():
              if servers_ooo[keys_network] == all_servers[keys_network]:
                since_time = min(since_time_list)
                if type(until_time) is int:
                  until_time_list.append(until_time)
                if until_time != 'now':
                  until_time = max(until_time_list)

                with open('output4.txt', 'a') as o:
                    print('Network "'+str(keys_network)+'" is down since '+since_time+' until '+until_time, file=o)


subnet_disorder_output("log4.txt", 3) #暫定的にfilename='log4.txt', N=3としています。実行する際に書き換えてください。