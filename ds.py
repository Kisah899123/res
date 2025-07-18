#!/usr/bin/env python3
"""
⚠️ AGGRESSIVE SERVER TESTING TOOL ⚠️
HANYA UNTUK TESTING SERVER YANG ANDA MILIKI!
JANGAN GUNAKAN PADA WEBSITE ORANG LAIN!

Fitur:
- Multiple path testing
- Unlimited requests
- Advanced bypass methods
- Server stress testing
"""

import requests
import time
import sys
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
import argparse
from bs4 import BeautifulSoup
import json

class AggressiveTester:
    """Tool untuk aggressive server testing"""
    
    def __init__(self, target_url, max_workers=10):
        self.target_url = target_url
        self.max_workers = max_workers
        self.session = requests.Session()
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        self.running = True
        
        # Setup session
        self._setup_session()
        
        # Common paths untuk testing
        self.common_paths = [
            # Admin paths
            '/admin', '/admin/', '/administrator', '/admin.php', '/admin.html',
            '/wp-admin', '/wp-admin/', '/wp-login.php', '/wp-admin/admin-ajax.php',
            '/admin/login', '/admin/dashboard', '/admin/users', '/admin/settings',
            
            # API paths
            '/api', '/api/', '/api/v1', '/api/v2', '/api/users', '/api/data',
            '/rest', '/rest/', '/graphql', '/graphql/', '/swagger', '/swagger/',
            
            # Database paths
            '/phpmyadmin', '/phpmyadmin/', '/mysql', '/mysql/', '/db', '/db/',
            '/database', '/database/', '/sql', '/sql/', '/myadmin', '/myadmin/',
            
            # File paths
            '/files', '/files/', '/uploads', '/uploads/', '/images', '/images/',
            '/static', '/static/', '/assets', '/assets/', '/media', '/media/',
            
            # Config paths
            '/config', '/config/', '/.env', '/.env.local', '/.env.production',
            '/config.php', '/config.json', '/config.xml', '/settings.php',
            
            # Backup paths
            '/backup', '/backup/', '/backups', '/backups/', '/bak', '/bak/',
            '/old', '/old/', '/archive', '/archive/', '/temp', '/temp/',
            
            # Log paths
            '/logs', '/logs/', '/log', '/log/', '/error.log', '/access.log',
            '/debug.log', '/system.log', '/app.log', '/web.log',
            
            # CMS paths
            '/wp-content', '/wp-content/', '/wp-includes', '/wp-includes/',
            '/joomla', '/joomla/', '/drupal', '/drupal/', '/magento', '/magento/',
            
            # Framework paths
            '/laravel', '/laravel/', '/symfony', '/symfony/', '/django', '/django/',
            '/rails', '/rails/', '/spring', '/spring/', '/express', '/express/',
            
            # Testing paths
            '/test', '/test/', '/testing', '/testing/', '/dev', '/dev/',
            '/development', '/development/', '/staging', '/staging/',
            
            # Common files
            '/robots.txt', '/sitemap.xml', '/favicon.ico', '/.htaccess',
            '/web.config', '/crossdomain.xml', '/clientaccesspolicy.xml',
            
            # Error pages
            '/404', '/404.html', '/500', '/500.html', '/error', '/error/',
            '/maintenance', '/maintenance/', '/under-construction', '/under-construction/',
            
            # Search paths
            '/search', '/search/', '/find', '/find/', '/query', '/query/',
            '/lookup', '/lookup/', '/browse', '/browse/', '/explore', '/explore/',
            
            # User paths
            '/user', '/user/', '/users', '/users/', '/profile', '/profile/',
            '/account', '/account/', '/login', '/login/', '/register', '/register/',
            
            # System paths
            '/system', '/system/', '/sys', '/sys/', '/core', '/core/',
            '/kernel', '/kernel/', '/boot', '/boot/', '/init', '/init/',
            
            # Cache paths
            '/cache', '/cache/', '/tmp', '/tmp/', '/temp', '/temp/',
            '/var', '/var/', '/tmp/cache', '/tmp/cache/', '/cache/tmp', '/cache/tmp/',
            
            # Custom paths (random)
            '/random', '/random/', '/test123', '/test123/', '/debug', '/debug/',
            '/info', '/info/', '/status', '/status/', '/health', '/health/',
            '/ping', '/ping/', '/pong', '/pong/', '/echo', '/echo/',
        ]
        
        # Additional random paths
        self.random_paths = [
            f'/{random.randint(1000, 9999)}',
            f'/path{random.randint(1, 100)}',
            f'/test{random.randint(1, 50)}',
            f'/api{random.randint(1, 10)}',
            f'/v{random.randint(1, 5)}',
            f'/beta{random.randint(1, 3)}',
            f'/alpha{random.randint(1, 3)}',
            f'/dev{random.randint(1, 10)}',
            f'/staging{random.randint(1, 5)}',
            f'/prod{random.randint(1, 3)}',
        ]
    
    def _setup_session(self):
        """Setup session dengan headers yang aggressive"""
        # Rotating User Agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
        ]
        
        # Headers yang aggressive
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'CF-Connecting-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
        })
        
        # Setup retry strategy
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504, 403, 407],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def test_path(self, path):
        """Test single path"""
        if not self.running:
            return None
            
        try:
            url = urljoin(self.target_url, path)
            
            # Randomize headers untuk setiap request
            self.session.headers['User-Agent'] = random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ])
            
            # Randomize IP
            self.session.headers['X-Forwarded-For'] = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
            
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            self.request_count += 1
            
            # Analyze response
            status = response.status_code
            content_length = len(response.content)
            
            if status == 200:
                self.success_count += 1
                print(f"✅ [{self.request_count}] {path} - Status: {status} - Size: {content_length}")
                
                # Check for interesting content
                if any(keyword in response.text.lower() for keyword in ['admin', 'login', 'password', 'database', 'config']):
                    print(f"🔍 INTERESTING: {path} contains sensitive keywords!")
                    
            elif status in [403, 404, 500, 502, 503]:
                self.failed_count += 1
                print(f"❌ [{self.request_count}] {path} - Status: {status} - Size: {content_length}")
                
            else:
                print(f"⚠️ [{self.request_count}] {path} - Status: {status} - Size: {content_length}")
            
            return {
                'path': path,
                'url': url,
                'status': status,
                'size': content_length,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies)
            }
            
        except Exception as e:
            self.failed_count += 1
            print(f"💥 [{self.request_count}] {path} - Error: {str(e)}")
            return None
    
    def generate_random_paths(self, count=100):
        """Generate random paths untuk testing"""
        paths = []
        
        # Common patterns
        patterns = [
            '/{word}{num}',
            '/{word}_{num}',
            '/{word}-{num}',
            '/{num}{word}',
            '/{word}/{num}',
            '/{num}/{word}',
        ]
        
        words = ['test', 'api', 'admin', 'user', 'data', 'file', 'config', 'backup', 'log', 'temp', 'cache', 'dev', 'prod', 'staging', 'beta', 'alpha']
        
        for i in range(count):
            pattern = random.choice(patterns)
            word = random.choice(words)
            num = random.randint(1, 9999)
            
            path = pattern.format(word=word, num=num)
            paths.append(path)
        
        return paths
    
    def start_unlimited_testing(self):
        """Mulai unlimited testing"""
        print(f"🚀 Memulai AGGRESSIVE TESTING pada: {self.target_url}")
        print(f"⚡ Max Workers: {self.max_workers}")
        print(f"⏰ Tanpa batas waktu - Tekan Ctrl+C untuk stop")
        print("=" * 60)
        
        all_paths = self.common_paths + self.random_paths
        
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                while self.running:
                    # Generate more random paths
                    random_paths = self.generate_random_paths(50)
                    current_paths = all_paths + random_paths
                    
                    # Submit tasks
                    futures = []
                    for path in current_paths:
                        if not self.running:
                            break
                        future = executor.submit(self.test_path, path)
                        futures.append(future)
                    
                    # Wait for completion
                    for future in as_completed(futures):
                        if not self.running:
                            break
                        result = future.result()
                        
                        # Print stats setiap 10 requests
                        if self.request_count % 10 == 0:
                            self.print_stats()
                    
                    # Small delay untuk menghindari rate limiting
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n⏹️ Testing dihentikan oleh user")
            self.running = False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.running = False
    
    def print_stats(self):
        """Print statistics"""
        elapsed_time = time.time() - self.start_time
        requests_per_second = self.request_count / elapsed_time if elapsed_time > 0 else 0
        
        print(f"\n📊 STATS - Requests: {self.request_count} | Success: {self.success_count} | Failed: {self.failed_count} | RPS: {requests_per_second:.2f}")
        print(f"⏱️ Elapsed: {elapsed_time:.1f}s | Running: {self.running}")
        print("-" * 60)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='⚠️ AGGRESSIVE SERVER TESTING TOOL ⚠️')
    parser.add_argument('url', help='Target URL (HANYA SERVER YANG ANDA MILIKI!)')
    parser.add_argument('--workers', type=int, default=10, help='Number of workers (default: 10)')
    parser.add_argument('--confirm', action='store_true', help='Confirm that you own this server')
    
    args = parser.parse_args()
    
    # Safety check
    if not args.confirm:
        print("⚠️  PERINGATAN KEAMANAN ⚠️")
        print("=" * 50)
        print("Tool ini HANYA untuk testing server yang ANDA MILIKI!")
        print("JANGAN GUNAKAN pada website orang lain!")
        print("Ini bisa dianggap sebagai serangan DDoS!")
        print("=" * 50)
        print(f"Target: {args.url}")
        print("=" * 50)
        
        confirm = input("Apakah Anda yakin server ini MILIK ANDA? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Testing dibatalkan")
            return
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Start testing
    tester = AggressiveTester(args.url, args.workers)
    
    try:
        tester.start_unlimited_testing()
    except KeyboardInterrupt:
        print("\n⏹️ Testing dihentikan")
    finally:
        tester.running = False
        tester.print_stats()
        print("\n🏁 Testing selesai")

if __name__ == "__main__":
    main() 
