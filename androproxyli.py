import requests
import os
import json
import time
import concurrent.futures
from urllib.parse import quote
import sys

PROXY_PREFIX = "https://proxy.freecdn.workers.dev/?url="  # 🔥 EKLENEN BÖLÜM

def test_proxy_speed(proxy_url, test_url="https://httpbin.org/ip", timeout=3):
    try:
        start_time = time.time()
        response = requests.get(test_url, timeout=timeout, 
                              proxies={"http": proxy_url, "https": proxy_url})
        if response.status_code == 200:
            speed = time.time() - start_time
            return proxy_url, speed, True
    except:
        pass
    return proxy_url, 10, False

def get_fastest_proxies():
    print("⚡ GitHub Actions için proxy test ediliyor...")
    
    workers = [
        ("CF-Proxy", "https://withered-shape-3305.vadimkantorov.workers.dev/?"),
        ("Rapid-Proxy", "https://rapid-wave-c8e3.redfor14314.workers.dev/"),
        ("Cors-Free", "https://proxy.freecdn.workers.dev/?url="),
        ("Hello-World", "https://hello-world-aged-resonance-fc8f.bokaflix.workers.dev/?apiUrl="),
        ("AllOrigins", "https://api.allorigins.win/raw?url="),
    ]
    
    fast_proxies = []
    for name, url in workers:
        fast_proxies.append(url)
        print(f"   ✅ {name} eklendi")
    
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("🚀 GitHub Actions ortamında çalışıyor")
        extra_workers = [
            "https://cors-anywhere.herokuapp.com/",
            "https://thingproxy.freeboard.io/fetch/",
            "https://yacdn.org/proxy/",
        ]
        fast_proxies.extend(extra_workers)
    
    fast_proxies.append("direct")
    return fast_proxies[:10]

def check_url_with_proxy(url, proxies, timeout=5):
    try:
        response = requests.head(url, timeout=timeout)
        if response.status_code == 200:
            return url, "direct"
    except:
        pass
    
    for proxy in proxies:
        if proxy == "direct":
            continue
            
        try:
            if proxy.endswith("?") or "?url=" in proxy or "?quest=" in proxy or "apiUrl=" in proxy or "/raw?url=" in proxy:
                proxy_url = f"{proxy}{quote(url, safe='')}" if "allorigins.win" in proxy else f"{proxy}{url}"
            elif "/proxy/" in proxy or "/fetch/" in proxy:
                proxy_url = f"{proxy}{url}"
            elif proxy.startswith("http://") or proxy.startswith("https://"):
                proxies_dict = {"http": proxy, "https": proxy}
                response = requests.head(url, timeout=timeout, proxies=proxies_dict)
                if response.status_code == 200:
                    return url, proxy
                continue
            else:
                continue
                
            response = requests.head(proxy_url, timeout=timeout)
            if response.status_code == 200:
                return proxy_url, proxy
        except:
            continue
    
    return None, None

def get_active_base_url(proxies):
    print("\n🔍 Aktif domain aranıyor...")
    
    priority_domains = [
        "https://andro.226503.xyz/checklist/",
        "https://androiptv.fun/checklist/",
        "https://birazcikspor.xyz/checklist/",
        "https://androstream.live/checklist/",
    ]
    
    test_channels = [
        "androstreamlivebs1",
        "androstreamlivess1",
        "androstreamlivets"
    ]
    
    for domain in priority_domains:
        for channel in test_channels:
            test_url = f"{domain}{channel}.m3u8"
            stream_url, used_proxy = check_url_with_proxy(test_url, proxies, timeout=3)
            if stream_url:
                print(f"✅ Aktif domain: {domain} (via {used_proxy})")
                return domain
    
    print("⚠  Öncelikli domainler çalışmıyor, alternatifler taranıyor...")
    
    for i in range(1, 30):
        domain = f"https://birazcikspor{i}.xyz/checklist/"
        test_url = f"{domain}androstreamlivebs1.m3u8"
        try:
            response = requests.head(test_url, timeout=2)
            if response.status_code == 200:
                print(f"✅ Alternatif domain: {domain}")
                return domain
        except:
            continue
    
    default_domain = "https://andro.226503.xyz/checklist/"
    print(f"⚠  Varsayılan domain: {default_domain}")
    return default_domain

def get_DeaTHLesS_streams():
    print("=" * 60)
    print("🚀 DeaTHLesS IPTV Bot - GitHub Actions Optimize")
    print("=" * 60)
    
    proxies = get_fastest_proxies()
    print(f"📊 Kullanılacak proxy sayısı: {len(proxies)}")
    
    base_url = get_active_base_url(proxies)
    
    print(f"\n📡 Kanal listesi oluşturuluyor: {base_url}")
    
    channels = get_channel_list()
    
    m3u_content = "#EXTM3U\n"
    m3u_content += "# DeaTHLesS IPTV - GitHub Actions\n"
    m3u_content += f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    m3u_content += f"# Base URL: {base_url}\n\n"
    
    successful = 0
    total = len(channels)
    
    for name, channel_id in channels:
        url = f"{base_url}{channel_id}.m3u8"
        stream_url, proxy_used = check_url_with_proxy(url, proxies)
        
        if stream_url:
            logo_url = "https://i.hizliresim.com/8xzjgqv.jpg"
            m3u_content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="TR:{name}" tvg-logo="{logo_url}" group-title="TURKIYE",{name}\n'
            
            # 🔥 TÜM LİNKLER BURADA ZORUNLU OLARAK PROXY PREFIX İLE YAZILIYOR
            m3u_content += f"{PROXY_PREFIX}{url}\n"

            successful += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name}")
    
    print(f"\n📊 Sonuç: {successful}/{total} kanal bulundu")
    
    if successful < 5:
        print("\n⚠ Çok az kanal bulundu, alternatif yöntem deneniyor...")
        alt_content = try_alternative_method(base_url)
        if alt_content:
            m3u_content += alt_content
            print("✅ Alternatif yöntemle kanallar eklendi")
    
    return m3u_content

def get_channel_list():
    return [
            ["beIN Sport 1 HD", "androstreamlivebs1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Facebook beIN Sport 1", "facebooklivebs1", "https://i.hizliresim.com/8xzjgqv.jpg"]],
            ["beIN Sport 2 HD", "androstreamlivebs2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["beIN Sport 3 HD", "androstreamlivebs3", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["beIN Sport 4 HD", "androstreamlivebs4", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["beIN Sport 5 HD", "androstreamlivebs5", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["beIN Sport Max 1 HD", "androstreamlivebsm1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["beIN Sport Max 2 HD", "androstreamlivebsm2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["beIN Sports Haber HD", "androstreamlivebsh", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["S Sport 1 HD", "androstreamlivess1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Facebook S Sport 1", "facebooklivess1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["S Sport 2 HD", "androstreamlivess2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["S Sport Plus 1 HD", "androstreamlivessp1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["S Sport Plus 2 HD", "androstreamlivessp2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tivibu Sport HD", "androstreamlivets", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tivibu Sport 1 HD", "androstreamlivets1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tivibu Sport 2 HD", "androstreamlivets2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tivibu Sport 3 HD", "androstreamlivets3", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tivibu Sport 4 HD", "androstreamlivets4", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Smart Sport 1 HD", "androstreamlivesm1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Smart Sport 2 HD", "androstreamlivesm2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Euro Sport 1 HD", "androstreamlivees1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Euro Sport 2 HD", "androstreamlivees2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["TRT Spor HD", "androstreamlivetrtspor", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["TRT Spor Yıldız HD", "androstreamlivetrtspory", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii HD", "androstreamlivetb", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 1 HD", "androstreamlivetb1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 2 HD", "androstreamlivetb2", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 3 HD", "androstreamlivetb3", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 4 HD", "androstreamlivetb4", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 5 HD", "androstreamlivetb5", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 6 HD", "androstreamlivetb6", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 7 HD", "androstreamlivetb7", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Tabii 8 HD", "androstreamlivetb8", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Exxen HD", "androstreamliveexn", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Exxen 1 HD", "androstreamliveexn1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["TRT 1 HD", "androstreamlivetrt1", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["ATV HD", "androstreamliveatv", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["Kanal D HD", "androstreamlivekanald", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["TV 8 HD", "androstreamlivetv8", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["A Spor HD", "androstreamliveaspor", "https://i.hizliresim.com/8xzjgqv.jpg"],
            ["NBA TV HD", "androstreamlivenba", "https://i.hizliresim.com/8xzjgqv.jpg"]
    ]

def try_alternative_method(base_url):
    content = ""
    
    channels = [
        ("beIN Sport 1", "androstreamlivebs1"),
        ("beIN Sport 2", "androstreamlivebs2"),
        ("S Sport 1", "androstreamlivess1"),
        ("Tivibu Sport", "androstreamlivets"),
    ]
    
    for name, channel_id in channels:
        url = f"{base_url}{channel_id}.m3u8"
        content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="{name}",{name}\n'
        content += f"{PROXY_PREFIX}{url}\n"  # 🔥 BURADA DA AYNI
    
    return content

def save_m3u_file(content):
    try:
        file_name = "androvpnsiz.m3u"
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        
        channel_count = content.count('#EXTINF')
        
        print("\n" + "=" * 60)
        print("✅ İŞLEM TAMAMLANDI!")
        print("=" * 60)
        print(f"📂 Dosya: {file_name}")
        print(f"📊 Toplam Kanal: {channel_count}")
        print(f"💾 Boyut: {len(content.encode('utf-8'))} bytes")
        
        return file_name
        
    except Exception as e:
        print(f"❌ Dosya kaydetme hatası: {e}")
        return None

if __name__ == "__main__":
    try:
        print(f"Python {sys.version}")
        print(f"Çalışma dizini: {os.getcwd()}")
        
        m3u_data = get_DeaTHLesS_streams()
        
        if m3u_data and m3u_data.count('#EXTINF') > 0:
            saved_file = save_m3u_file(m3u_data)
            
            print("\n📋 İlk 5 kanal:")
            lines = m3u_data.split('\n')
            count = 0
            for line in lines:
                if line.startswith('#EXTINF') and count < 5:
                    name = line.split(',')[-1]
                    print(f"  {count+1}. {name}")
                    count += 1
            
        else:
            print("\n❌ HATA: Hiç kanal bulunamadı!")
            
    except KeyboardInterrupt:
        print("\n⏹ İşlem durduruldu")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
