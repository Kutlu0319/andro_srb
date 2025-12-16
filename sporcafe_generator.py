import requests
import urllib3
import re
from datetime import datetime
import json

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Kanal bilgileri
CHANNEL_INFO = {
     {"id": "sbeinsports-1", "name": "BeIN Sports 1", "tvg_id": "bein1", "logo": "https://r2.thesportsdb.com/images/media/channel/logo/5rhmw31628798883.png", "group": "BEIN SPORTS"},
        {"id": "sbeinsports-2", "name": "BeIN Sports 2", "tvg_id": "bein2", "logo": "https://r2.thesportsdb.com/images/media/channel/logo/7uv6x71628799003.png", "group": "BEIN SPORTS"},
        {"id": "sbeinsports-3", "name": "BeIN Sports 3", "tvg_id": "bein3", "logo": "https://r2.thesportsdb.com/images/media/channel/logo/u3117i1628798857.png", "group": "BEIN SPORTS"},
        {"id": "sbeinsports-4", "name": "BeIN Sports 4", "tvg_id": "bein4", "logo": "https://i.postimg.cc/0yjyF10x/bein4.png", "group": "BEIN SPORTS"},
        {"id": "sbeinsports-5", "name": "BeIN Sports 5", "tvg_id": "bein5", "logo": "https://i.postimg.cc/BvjF7hx5/bein5.png", "group": "BEIN SPORTS"},
        {"id": "sbeinsportshaber", "name": "BeIN Sports Haber", "tvg_id": "beinhd", "logo": "https://i.postimg.cc/x14Fs2kw/beinhd.png", "group": "BEIN SPORTS"},
        {"id": "sdazn1", "name": "DAZN 1", "tvg_id": "dazn1", "logo": "https://i.postimg.cc/QMgmHh7x/dazn1.png", "group": "DAZN"},
        {"id": "sdazn2", "name": "DAZN 2", "tvg_id": "dazn2", "logo": "https://i.postimg.cc/XY5YQvSd/dazn2.png", "group": "DAZN"},
        {"id": "saspor", "name": "A Spor", "tvg_id": "aspor", "logo": "https://i.postimg.cc/gJMK4kTN/aspor.png", "group": "YEREL SPOR"},
        {"id": "sssport", "name": "S Sport", "tvg_id": "ssport", "logo": "https://i.postimg.cc/TYcZT4zR/ssport.png", "group": "S SPORT"},
        {"id": "sssport2", "name": "S Sport 2", "tvg_id": "ssport2", "logo": "https://i.postimg.cc/WbftnShM/ssport2.png", "group": "S SPORT"},
        {"id": "sssplus1", "name": "S Sport Plus", "tvg_id": "ssportplus", "logo": "https://i.postimg.cc/rmK04Jxr/ssportplus.png", "group": "S SPORT"},
        {"id": "strtspor", "name": "TRT Spor", "tvg_id": "trtspor", "logo": "https://i.postimg.cc/jjTfdSTL/trtspor.png", "group": "TRT"},
        {"id": "strtspor2", "name": "TRT Spor 2", "tvg_id": "trtspor2", "logo": "https://i.postimg.cc/wvsvstyn/trtspor2.png", "group": "TRT"},
        {"id": "stv8", "name": "TV8", "tvg_id": "tv8", "logo": "https://i.postimg.cc/CLpftN9Y/tv8.png", "group": "DİĞER"},
        {"id": "sexxen-1", "name": "Exxen Spor 1", "tvg_id": "exxen1", "logo": "https://i.postimg.cc/B6t4z1d3/exxen.png", "group": "EXXEN"},
        {"id": "sexxen-2", "name": "Exxen Spor 2", "tvg_id": "exxen2", "logo": "https://i.postimg.cc/B6t4z1d3/exxen.png", "group": "EXXEN"},
        {"id": "ssmartspor", "name": "Smart Spor", "tvg_id": "smartspor", "logo": "https://i.postimg.cc/7YNxxHgM/smartspor.png", "group": "DİĞER"},
        {"id": "ssmartspor2", "name": "Smart Spor 2", "tvg_id": "smartspor2", "logo": "https://i.postimg.cc/7YNxxHgM/smartspor.png", "group": "DİĞER"},
        {"id": "stivibuspor-1", "name": "Tivibu Spor 1", "tvg_id": "tivibu1", "logo": "https://i.postimg.cc/G2xMf9Gn/tivibu.png", "group": "TİVİBU"},
        {"id": "stivibuspor-2", "name": "Tivibu Spor 2", "tvg_id": "tivibu2", "logo": "https://i.postimg.cc/G2xMf9Gn/tivibu.png", "group": "TİVİBU"},
        {"id": "stivibuspor-3", "name": "Tivibu Spor 3", "tvg_id": "tivibu3", "logo": "https://i.postimg.cc/G2xMf9Gn/tivibu.png", "group": "TİVİBU"},
        {"id": "stivibuspor-4", "name": "Tivibu Spor 4", "tvg_id": "tivibu4", "logo": "https://i.postimg.cc/G2xMf9Gn/tivibu.png", "group": "TİVİBU"},
        {"id": "stabiispor-1", "name": "Tabii Spor 1", "tvg_id": "tabii1", "logo": "https://i.postimg.cc/9MpztRQF/tabii.png", "group": "TABII"},
        {"id": "stabiispor-2", "name": "Tabii Spor 2", "tvg_id": "tabii2", "logo": "https://i.postimg.cc/9MpztRQF/tabii.png", "group": "TABII"},
        {"id": "stabiispor-3", "name": "Tabii Spor 3", "tvg_id": "tabii3", "logo": "https://i.postimg.cc/9MpztRQF/tabii.png", "group": "TABII"},
        {"id": "stabiispor-4", "name": "Tabii Spor 4", "tvg_id": "tabii4", "logo": "https://i.postimg.cc/9MpztRQF/tabii.png", "group": "TABII"},
        {"id": "stabiispor-5", "name": "Tabii Spor 5", "tvg_id": "tabii5", "logo": "https://i.postimg.cc/9MpztRQF/tabii.png", "group": "TABII"},
        {"id": "strt1", "name": "TRT 1", "tvg_id": "trt1", "logo": "https://i.postimg.cc/XYJkFyqV/trt1.png", "group": "TRT"},
}

def fetch_url(url):
    """URL'den içerik çek"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        return response.text
    except Exception as e:
        print(f"✗ Error fetching {url}: {e}")
        return None

def get_active_domain():
    """Aktif domain'i bul"""
    print("🔍 Searching for active domain...")
    for i in range(15, 4, -1):
        url = f"https://www.sporcafe{i}.xyz/"
        print(f"  Trying: {url}")
        html = fetch_url(url)
        if html and len(html) > 1000:
            print(f"  ✓ Active domain found: {url}")
            return {'url': url, 'html': html}
    return None

def get_stream_domain(html):
    """HTML'den stream domain'ini bul"""
    patterns = [
        r'https?:\/\/(main\.uxsyplayer[0-9a-zA-Z\-]+\.click)',
        r'https?:\/\/(main\.[0-9a-zA-Z\-]+\.click)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return f"https://{match.group(1)}"
    return None

def get_all_channels_from_html(html):
    """HTML'den tüm kanal ID'lerini çıkar"""
    matches = re.findall(r'data-stream-url="([^"]+)"', html)
    return list(set(matches)) if matches else list(CHANNEL_INFO.keys())

def get_stream_links(domain_info, channels):
    """Stream linklerini al"""
    print("🔗 Fetching stream links...")
    stream_domain = get_stream_domain(domain_info['html']) or "https://main.uxsyplayer1.click"
    print(f"  Stream domain: {stream_domain}")

    results = {}
    successful = 0

    for i, channel in enumerate(channels, 1):
        channel_id = channel['id']
        print(f"  [{i}/{len(channels)}] {channel['name']}")
        channel_url = f"{stream_domain}/index.php?id={channel_id}"
        html = fetch_url(channel_url)

        if html:
            ads_match = re.search(r'this\.adsBaseUrl\s*=\s*[\'"]([^\'"]+)', html)
            if ads_match:
                base_url = ads_match.group(1).rstrip('/') + '/'
                stream_url = f"{base_url}{channel_id}/playlist.m3u8"
                results[channel_id] = {
                    'url': stream_url,
                    'name': channel['name'],
                    'tvg_id': channel['tvg_id'],
                    'logo': channel['logo'],
                    'group': channel['group']
                }
                successful += 1
                print(f"      ✓ Stream found")

    print(f"📊 Success: {successful}/{len(channels)} streams")
    return {
        'referer': domain_info['url'],
        'stream_domain': stream_domain,
        'channels': results,
        'total': len(channels),
        'successful': successful
    }

def generate_m3u(stream_info):
    """M3U playlist oluştur"""
    print("📝 Generating M3U playlist...")
    output = ["#EXTM3U"]

    sorted_channels = sorted(
        stream_info['channels'].items(),
        key=lambda x: x[1]['name']
    )

    for channel_id, channel_data in sorted_channels:
        group = "SPOR"
        if 'beinsports' in channel_id: group = "BeIN SPORTS"
        elif 'dazn' in channel_id: group = "DAZN"
        elif 'ssport' in channel_id: group = "S SPORT"
        elif 'trt' in channel_id: group = "TRT"
        elif 'exxen' in channel_id: group = "EXXEN"
        elif 'tivibu' in channel_id: group = "TIVIBU"
        elif 'tabii' in channel_id: group = "TABII"

        extinf = f'#EXTINF:-1 tvg-id="{channel_data["tvg_id"]}" tvg-name="{channel_data["name"]}" tvg-logo="{channel_data["logo"]}" group-title="{group}",{channel_data["name"]}'
        output.append(extinf)
        output.append(f'#EXTVLCOPT:http-referrer={stream_info["referer"]}')
        output.append(channel_data['url'])
        output.append("")

    return "\n".join(output)

def main():
    print("=" * 60)
    print("SPORCAFE M3U GENERATOR")
    print("=" * 60)

    # Kanal listesi (örnek)
    channels = list(CHANNEL_INFO.values())

    # Aktif domain
    domain_info = get_active_domain()
    if not domain_info:
        print("✗ ERROR: No active domain found!")
        return

    print(f"✓ Active domain: {domain_info['url']}")

    # Stream linklerini al
    stream_info = get_stream_links(domain_info, channels)
    if not stream_info['channels']:
        print("✗ ERROR: No stream links found!")
        return

    print(f"✓ Found {stream_info['successful']} streams")

    # M3U oluştur
    m3u_content = generate_m3u(stream_info)
    with open('sporcafe.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print("✓ M3U file saved: sporcafe.m3u")

    # JSON kaydet
    json_data = {
        'generated': datetime.now().isoformat(),
        'domain': domain_info['url'],
        'channels_count': stream_info['successful'],
        'channels': list(stream_info['channels'].values())
    }
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print("✓ JSON file saved: channels.json")

    # Örnek M3U
    print("\nExample M3U format (first 3 channels):")
    lines = m3u_content.split('\n')[:12]
    for line in lines:
        print(line)

if __name__ == "__main__":
    main()
