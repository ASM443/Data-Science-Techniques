import subprocess
import re
import platform
import networkx as nx
import matplotlib.pyplot as plt

def trace_route(url):
    try:
        command = "tracert"

        # Run the command
        trace_result = subprocess.check_output([command, url]).decode('utf-8')

        # Parse the output to find hostnames, IP addresses
        hostnames = re.findall(r'\n\s*\d+\s+([\w.-]+)', trace_result)
        ip_addresses = re.findall(r'\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]', trace_result) if command == "tracert" else re.findall(r'\(([\d.]+)\)', trace_result)

        return list(zip(hostnames, ip_addresses))

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def create_graph(servers_list):
    G = nx.DiGraph()

    for servers in servers_list:
        for i in range(len(servers) - 1):
            G.add_edge(servers[i][1], servers[i + 1][1])

    return G

def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, font_weight='bold', node_size=1000)
    plt.axis("off")
    plt.show()

def print_servers(url, servers):
    print(f"\nServers touched to reach '{url}':")
    for index, server in enumerate(servers, start=1):
        print(f"{index}. {server[0]} ({server[1]})")

def save_graph_to_gexf(G, filename):
    nx.write_gexf(G, filename)

websites = ["www.google.com", "www.youtube.com", "www.facebook.com", "www.twitter.com", "www.instagram.com", "www.baidu.com", "www.wikipedia.org", "www.yandex.ru", "www.yahoo.com", "www.whatsapp.com", "www.xvideos.com", "www.pornhub.com", "www.amazon.com", "www.xnxx.com", "www.live.com", "www.tiktok.com", "www.docomo.ne.jp", "www.yahoo.co.jp", "www.linkedin.com", "www.reddit.com", "www.openai.com", "www.office.com", "www.netflix.com", "www.dzen.ru", "www.bing.com", "www.vk.com", "www.xhamster.com", "www.microsoftonline.com", "www.samsung.com", "www.mail.ru", "www.naver.com", "www.turbopages.org", "www.weather.com", "www.discord.com", "www.twitch.tv", "www.pinterest.com", "www.bilibili.com", "www.microsoft.com", "www.zoom.us", "www.duckduckgo.com", "www.realsrv.com", "www.qq.com", "www.quora.com", "www.roblox.com", "www.msn.com", "www.fandom.com", "www.sharepoint.com", "www.ebay.com", "www.aajtak.in", "www.globo.com"]

servers_list = [trace_route(url) for url in websites]
for url, servers in zip(websites, servers_list):
    print_servers(url, servers)

graph = create_graph(servers_list)
draw_graph(graph)

gexf_filename = "output_graph.gexf"
save_graph_to_gexf(graph, gexf_filename)
print(f"\nGraph saved to '{gexf_filename}'.")