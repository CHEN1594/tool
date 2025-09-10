import requests
from bs4 import BeautifulSoup

# ============ 获取 GitHub 链接和 Stars ============


def find_github_links(arxiv_html_url):
    """在 arXiv HTML 页面中查找所有 GitHub 链接"""
    response = requests.get(arxiv_html_url)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    github_links = [
        link for link in links if link.startswith("https://github.com")]
    return github_links


def get_github_stars(repo_url):
    """通过 GitHub API 获取 Star 数量"""
    try:
        parts = repo_url.split("/")
        owner, repo = parts[3], parts[4]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        r = requests.get(api_url)
        if r.status_code == 200:
            return r.json().get("stargazers_count", 0)
    except Exception as e:
        print(f"解析 GitHub 地址失败: {repo_url}, 错误: {e}")
    return None


# ============ 获取引用量 ============

def get_citation_count(arxiv_id):
    """通过 Semantic Scholar API 获取引用数"""
    url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields=title,citationCount,url"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return data.get("citationCount", 0), data.get("title", "N/A"), data.get("url", "")
    else:
        return None, None, None


# ============ 主流程 ============

def process_arxiv_id(arxiv_id):
    """处理单个 arXiv ID，输出 GitHub 链接 + Star + Citation"""
    print(f"\n====== arXiv:{arxiv_id} ======")

    # Citation
    citation, title, semantic_url = get_citation_count(arxiv_id)
    print(f"Title: {title}")
    print(f"Citations: {citation}")
    print(f"Semantic Scholar: {semantic_url}")

    # HTML 页面（自动跳转到最新版本）
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    r = requests.get(html_url)
    if r.status_code != 200:
        print("无 HTML 页面")
        print("-" * 60)
        return

    print(f"HTML Page: {html_url}")

    # GitHub
    github_links = find_github_links(html_url)
    if not github_links:
        print("未找到 GitHub 链接")
    else:
        for link in github_links:
            stars = get_github_stars(link)
            print(f"GitHub Repo: {link}")
            print(f"Stars: {stars}")
    print("-" * 60)


# ============ 主程序入口 ============

if __name__ == "__main__":
    arxiv_ids = [
        "2508.13998",
        "2505.16196",
        "2505.03238",
        "2505.16517",
        "2502.05855",
        "2505.23450",
        "2508.21112",
        "2507.16815",
        "2506.00070",
        "2504.19854",
        "2504.07615",
        "2507.10548"
    ]

    for arxiv_id in arxiv_ids:
        process_arxiv_id(arxiv_id)
