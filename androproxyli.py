import requests
import re
import os
import json

def get_DeaTHLesS_streams():
    """DeaTHLesS IPTV stream'lerini al"""
    
    print("🔍 Aktif domain aranıyor...")
    active_domain = None
    for i in range(42, 200):
        url = f"https://birazcikspor{i}.xyz/"
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                active_domain = url
                print(f"✅ Aktif domain bulundu: {active_domain}")
                break
        except:
            continue
    
    if not active_domain:
        print("❌ Aktif domain bulunamadı")
        return ""
    
    # Keşfedilen base URL
    base_url = "https://andro.226503.xyz/checklist/"
    print(f"🎯 Kullanılan base URL: {base_url}")
    
    return create_m3u_with_baseurl(base_url)

def create_m3u_with_baseurl(base_url):
    """Base URL ile M3U içeriği oluştur"""
    m3u_content = ""
    
    # Proxy listesi
    proxies = [
        "https://rapid-wave-c8e3.redfor14314.workers.dev/",
        "https://proxy.ponelat.workers.dev/",
        "https://proxy.freecdn.workers.dev/?url=",
        "https://withered-shape-3305.vadimkantorov.workers.dev/?",
        "https://wandering-sky-a896.cbracketdash.workers.dev/?",
        "https://hello-world-aged-resonance-fc8f.bokaflix.workers.dev/?apiUrl=",
        "https://cors.gerhut.workers.dev/?"
    ]
    
    # Ana kanal listesi
    channels = [
        # Spor Kanalları
        ["beIN Sport 1 HD", "androstreamlivebs1"],
        ["beIN Sport 2 HD", "androstreamlivebs2"],
        ["beIN Sport 3 HD", "androstreamlivebs3"],
        ["beIN Sport 4 HD", "androstreamlivebs4"],
        ["beIN Sport 5 HD", "androstreamlivebs5"],
        ["beIN Sport Max 1 HD", "androstreamlivebsm1"],
        ["beIN Sport Max 2 HD", "androstreamlivebsm2"],
        ["S Sport 1 HD", "androstreamlivess1"],
        ["S Sport 2 HD", "androstreamlivess2"],
        ["Tivibu Sport HD", "androstreamlivets"],
        ["Tivibu Sport 1 HD", "androstreamlivets1"],
        ["Tivibu Sport 2 HD", "androstreamlivets2"],
        ["Tivibu Sport 3 HD", "androstreamlivets3"],
        ["Tivibu Sport 4 HD", "androstreamlivets4"],
        ["Smart Sport 1 HD", "androstreamlivesm1"],
        ["Smart Sport 2 HD", "androstreamlivesm2"],
        ["Euro Sport 1 HD", "androstreamlivees1"],
        ["Euro Sport 2 HD", "androstreamlivees2"],
        
        # Dijital Platformlar
        ["Tabii HD", "androstreamlivetb"],
        ["Tabii 1 HD", "androstreamlivetb1"],
        ["Tabii 2 HD", "androstreamlivetb2"],
        ["Tabii 3 HD", "androstreamlivetb3"],
        ["Tabii 4 HD", "androstreamlivetb4"],
        ["Tabii 5 HD", "androstreamlivetb5"],
        ["Tabii 6 HD", "androstreamlivetb6"],
        ["Tabii 7 HD", "androstreamlivetb7"],
        ["Tabii 8 HD", "androstreamlivetb8"],
        ["Exxen HD", "androstreamliveexn"],
        ["Exxen 1 HD", "androstreamliveexn1"],
        ["Exxen 2 HD", "androstreamliveexn2"],
        ["Exxen 3 HD", "androstreamliveexn3"],
        ["Exxen 4 HD", "androstreamliveexn4"],
        ["Exxen 5 HD", "androstreamliveexn5"],
        ["Exxen 6 HD", "androstreamliveexn6"],
        ["Exxen 7 HD", "androstreamliveexn7"],
        ["Exxen 8 HD", "androstreamliveexn8"],
        
        # Facebook Stream'leri
        ["Facebook beIN Sport 1", "facebooklivebs1"],
        ["Facebook beIN Sport 2", "facebooklivebs2"],
        ["Facebook S Sport 1", "facebooklivess1"],
        ["Facebook Tivibu Sport", "facebooklivets"],
    ]
    
    successful_channels = []
    logo_url = "https://i.hizliresim.com/8xzjgqv.jpg"
    
    print(f"🔗 {len(channels)} kanal test ediliyor...")
    
    for channel_name, channel_id in channels:
        original_url = f"{base_url}{channel_id}.m3u8"
        stream_added = False
        
        # Önce doğrudan dene
        try:
            response = requests.head(original_url, timeout=5)
            if response.status_code == 200:
                m3u_content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="TR:{channel_name}" tvg-logo="{logo_url}" group-title="TURKIYE DEATHLESS",TR:{channel_name}\n'
                m3u_content += f"{original_url}\n"
                successful_channels.append(channel_name)
                print(f"✅ {channel_name}")
                stream_added = True
        except:
            pass
        
        # Proxy gerekirse
        if not stream_added:
            for proxy in proxies:
                try:
                    if "?url=" in proxy or proxy.endswith("?") or "apiUrl=" in proxy:
                        proxy_url = f"{proxy}{original_url}"
                    else:
                        proxy_url = f"{proxy}{original_url}"
                    
                    response = requests.head(proxy_url, timeout=5)
                    if response.status_code == 200:
                        m3u_content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="TR:{channel_name}" tvg-logo="{logo_url}" group-title="TURKIYE DEATHLESS",TR:{channel_name}\n'
                        m3u_content += f"{proxy_url}\n"
                        successful_channels.append(channel_name)
                        print(f"✅ {channel_name} (Proxy)")
                        stream_added = True
                        break
                except:
                    continue
            
            if not stream_added:
                print(f"❌ {channel_name}")
    
    print(f"\n📊 Toplam bulunan kanal: {len(successful_channels)}/{len(channels)}")
    
    # Ek kanal keşfi
    if successful_channels:
        print("\n🔍 Ek kanallar keşfediliyor...")
        additional = discover_additional_channels(base_url, proxies, logo_url)
        if additional:
            m3u_content += additional
            print(f"➕ Ek {len(additional.split('#EXTINF'))-1} kanal eklendi")
    
    return m3u_content

def discover_additional_channels(base_url, proxies, logo_url):
    """Ek kanalları keşfet"""
    additional_content = ""
    
    # Pattern'ler ve numara aralıkları
    patterns = {
        "androstreamlivebs": (1, 10),   # beIN Sports
        "androstreamlivess": (1, 5),    # S Sports  
        "androstreamlivets": (1, 10),   # Tivibu Sports
        "androstreamlivees": (1, 5),    # Euro Sports
        "androstreamliveexn": (1, 10),  # Exxen
        "androstreamlivetb": (1, 10),   # Tabii
        "androstreamlivesm": (1, 5),    # Smart Sport
        "facebooklivebs": (1, 5),       # Facebook beIN
        "facebooklivess": (1, 5),       # Facebook S Sport
        "facebooklivets": (1, 5),       # Facebook Tivibu
    }
    
    discovered = 0
    
    for pattern, (start, end) in patterns.items():
        for i in range(start, end + 1):
            channel_id = f"{pattern}{i}"
            channel_name = f"{pattern}{i}"
            
            # Zaten eklenmiş mi kontrol et
            if f"{channel_id}.m3u8" in additional_content:
                continue
                
            test_url = f"{base_url}{channel_id}.m3u8"
            
            # Test et
            for method in ['direct'] + proxies:
                try:
                    if method == 'direct':
                        response = requests.head(test_url, timeout=3)
                    else:
                        proxy_url = f"{method}{test_url}" if "?url=" in method or method.endswith("?") or "apiUrl=" in method else f"{method}{test_url}"
                        response = requests.head(proxy_url, timeout=3)
                    
                    if response.status_code == 200:
                        additional_content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="TR:{channel_name}" tvg-logo="{logo_url}" group-title="TURKIYE DEATHLESS",TR:{channel_name}\n'
                        additional_content += f"{test_url}\n"
                        discovered += 1
                        print(f"   🔍 Keşfedildi: {channel_id}")
                        break
                except:
                    continue
    
    if discovered:
        print(f"   🎯 Toplam keşfedilen: {discovered} kanal")
    
    return additional_content

def save_m3u_file(content, output_dir="output"):
    """M3U dosyasını kaydet"""
    try:
        # Output klasörünü oluştur
        os.makedirs(output_dir, exist_ok=True)
        
        # Ana M3U dosyası
        file_path = os.path.join(output_dir, "DeaTHlesS-Androiptv.m3u")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            f.write(content)
        
        # JSON formatında da kaydet (opsiyonel)
        json_path = os.path.join(output_dir, "channels.json")
        channels = []
        lines = content.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith('#EXTINF'):
                channel_info = lines[i]
                if i+1 < len(lines) and not lines[i+1].startswith('#'):
                    channels.append({
                        "name": channel_info.split(',')[-1] if ',' in channel_info else channel_info,
                        "url": lines[i+1],
                        "info": channel_info
                    })
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "total_channels": len(channels),
                "channels": channels,
                "generated_at": os.path.getctime(file_path)
            }, f, indent=2, ensure_ascii=False)
        
        # Dosya boyutunu kontrol et
        file_size = os.path.getsize(file_path)
        print(f"\n💾 M3U dosyası kaydedildi: {file_path}")
        print(f"📁 Dosya boyutu: {file_size} bytes")
        print(f"📊 Toplam kanal: {content.count('#EXTINF')}")
        
        return file_path
    except Exception as e:
        print(f"❌ Dosya kaydetme hatası: {e}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 DeaTHLesS IPTV Bot - BirazcikSpor Stream")
    print("=" * 50)
    
    m3u_data = get_DeaTHLesS_streams()
    
    if m3u_data:
        saved_file = save_m3u_file(m3u_data, output_dir=".")
        if saved_file:
            print(f"\n📂 Dosya: {os.path.basename(saved_file)}")
            print(f"📂 Klasör: {os.path.dirname(saved_file)}")
            
            # GitHub için özel mesaj
            print("\n" + "=" * 50)
            print("✅ GITHUB ACTIONS İŞLEMİ TAMAMLANDI!")
            print("=" * 50)
            print("\n📡 M3U dosyası oluşturuldu!")
            print("📤 Dosya repo'ya otomatik commit edilecek.")
            
            # Dosya içeriğini göster (ilk 5 kanal)
            print("\n📺 İlk 5 kanal:")
            lines = m3u_data.split('\n')
            count = 0
            for line in lines:
                if line.startswith('#EXTINF'):
                    print(f"   • {line.split(',')[-1]}")
                    count += 1
                    if count >= 5:
                        break
        else:
            print("\n❌ M3U dosyası oluşturulamadı!")
    else:
        print("\n❌ Kaydedilecek veri bulunamadı!")
    
    # GitHub Actions için başarılı çıkış kodu
    exit(0)
