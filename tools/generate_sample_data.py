"""
Generate realistic sample data for dashboard testing.
This simulates what the scrapers would produce with live data.
"""

import hashlib
import json
import os
from datetime import datetime, timezone, timedelta
import random

def make_id(url):
    return hashlib.sha256(url.encode()).hexdigest()[:16]

now = datetime.now(timezone.utc)

SAMPLE_ARTICLES = [
    # Reddit - r/artificial
    {
        "title": "Google DeepMind announces Gemini 2.5 Ultra with breakthrough reasoning capabilities",
        "url": "https://www.reddit.com/r/artificial/comments/abc123/google_deepmind_announces_gemini_25_ultra",
        "summary": "Google DeepMind has unveiled Gemini 2.5 Ultra, claiming significant advances in multi-step reasoning, code generation, and multimodal understanding. The model reportedly outperforms GPT-5 on several benchmarks.",
        "source": "r/artificial",
        "source_type": "reddit",
        "author": "ai_researcher_42",
        "score": 2847,
        "comments_count": 534,
        "thumbnail": None,
        "tags": ["artificial", "reddit"],
    },
    {
        "title": "The EU AI Act enforcement begins today - here's what changes for developers",
        "url": "https://www.reddit.com/r/artificial/comments/def456/eu_ai_act_enforcement",
        "summary": "Starting today, the EU AI Act's first provisions go into effect. High-risk AI systems now require conformity assessments, and companies face fines up to 7% of global turnover for violations.",
        "source": "r/artificial",
        "source_type": "reddit",
        "author": "policy_watcher",
        "score": 1523,
        "comments_count": 287,
        "thumbnail": None,
        "tags": ["artificial", "reddit"],
    },
    {
        "title": "Anthropic releases Claude's system prompt - a masterclass in AI alignment",
        "url": "https://www.reddit.com/r/artificial/comments/ghi789/anthropic_releases_claudes_system_prompt",
        "summary": "Anthropic has publicly shared the full system prompt used for Claude, offering unprecedented transparency into how a major AI company approaches model behavior and safety guidelines.",
        "source": "r/artificial",
        "source_type": "reddit",
        "author": "alignment_advocate",
        "score": 3421,
        "comments_count": 612,
        "thumbnail": None,
        "tags": ["artificial", "reddit"],
    },
    # Reddit - r/MachineLearning
    {
        "title": "[R] Attention Is All You Need Was Wrong: New Architecture Outperforms Transformers",
        "url": "https://www.reddit.com/r/MachineLearning/comments/jkl012/attention_is_all_you_need_wrong",
        "summary": "Researchers at Stanford propose a novel architecture that replaces self-attention with a state-space model variant, achieving 15% better perplexity on language modeling tasks while being 3x faster at inference.",
        "source": "r/MachineLearning",
        "source_type": "reddit",
        "author": "ml_phd_student",
        "score": 4156,
        "comments_count": 891,
        "thumbnail": None,
        "tags": ["MachineLearning", "reddit"],
    },
    {
        "title": "[D] How are you handling the compute cost crisis? Sharing our optimization playbook",
        "url": "https://www.reddit.com/r/MachineLearning/comments/mno345/compute_cost_crisis_optimization",
        "summary": "Our team reduced training costs by 60% using a combination of mixed-precision training, gradient checkpointing, and a novel data loading pipeline. Sharing our full playbook.",
        "source": "r/MachineLearning",
        "source_type": "reddit",
        "author": "infra_lead_ml",
        "score": 1876,
        "comments_count": 234,
        "thumbnail": None,
        "tags": ["MachineLearning", "reddit"],
    },
    # Reddit - r/singularity
    {
        "title": "Sam Altman: 'We're closer to AGI than most people realize' - Full interview analysis",
        "url": "https://www.reddit.com/r/singularity/comments/pqr678/sam_altman_agi_closer_than_people_realize",
        "summary": "In a wide-ranging interview with Lex Fridman, Sam Altman discussed OpenAI's internal AGI timeline estimates, claiming that recent breakthroughs have accelerated their projections significantly.",
        "source": "r/singularity",
        "source_type": "reddit",
        "author": "singularity_now",
        "score": 5234,
        "comments_count": 1203,
        "thumbnail": None,
        "tags": ["singularity", "reddit"],
    },
    {
        "title": "The economic impact of AI automation is already visible in Q1 2026 earnings reports",
        "url": "https://www.reddit.com/r/singularity/comments/stu901/ai_automation_q1_2026_earnings",
        "summary": "Multiple Fortune 500 companies are reporting 20-40% productivity gains from AI integration. Goldman Sachs estimates AI will add $7 trillion to global GDP by 2030.",
        "source": "r/singularity",
        "source_type": "reddit",
        "author": "econ_futurist",
        "score": 2341,
        "comments_count": 456,
        "thumbnail": None,
        "tags": ["singularity", "reddit"],
    },
    # Reddit - r/ChatGPT
    {
        "title": "GPT-5 first impressions megathread: What's actually improved?",
        "url": "https://www.reddit.com/r/ChatGPT/comments/vwx234/gpt5_first_impressions_megathread",
        "summary": "Collecting early user reports on GPT-5's capabilities. Key improvements: much better at following complex instructions, reduced hallucination, and native tool use without plugins.",
        "source": "r/ChatGPT",
        "source_type": "reddit",
        "author": "gpt_power_user",
        "score": 6789,
        "comments_count": 2341,
        "thumbnail": None,
        "tags": ["ChatGPT", "reddit"],
    },
    {
        "title": "I built a complete SaaS in 2 days using Claude Code - here's my honest review",
        "url": "https://www.reddit.com/r/ChatGPT/comments/yza567/built_saas_2_days_claude_code_review",
        "summary": "Full breakdown of building a production SaaS from scratch using AI coding assistants. Includes what worked, what didn't, and where I still needed to manually intervene.",
        "source": "r/ChatGPT",
        "source_type": "reddit",
        "author": "indie_hacker_ai",
        "score": 3456,
        "comments_count": 567,
        "thumbnail": None,
        "tags": ["ChatGPT", "reddit"],
    },
    # Reddit - r/LocalLLaMA
    {
        "title": "Llama 4 Scout runs at 90 tokens/sec on a single RTX 5090 - benchmarks inside",
        "url": "https://www.reddit.com/r/LocalLLaMA/comments/bcd890/llama4_scout_90tps_rtx5090_benchmarks",
        "summary": "Detailed benchmarks of Meta's Llama 4 Scout (17B active params) on consumer hardware. GGUF quantization + speculative decoding makes local inference surprisingly practical.",
        "source": "r/LocalLLaMA",
        "source_type": "reddit",
        "author": "local_inference_lab",
        "score": 4567,
        "comments_count": 789,
        "thumbnail": None,
        "tags": ["LocalLLaMA", "reddit"],
    },
    {
        "title": "Open source model comparison chart - April 2026 edition",
        "url": "https://www.reddit.com/r/LocalLLaMA/comments/efg123/open_source_model_comparison_april_2026",
        "summary": "Updated comparison of all major open-source LLMs including Llama 4, Mistral Large 3, Qwen 3, and DeepSeek V4. Covers benchmarks, VRAM requirements, and licensing.",
        "source": "r/LocalLLaMA",
        "source_type": "reddit",
        "author": "model_curator",
        "score": 2890,
        "comments_count": 345,
        "thumbnail": None,
        "tags": ["LocalLLaMA", "reddit"],
    },
    # Ben's Bites
    {
        "title": "The AI infrastructure gold rush is creating a new class of billion-dollar startups",
        "url": "https://bensbites.beehiiv.com/p/ai-infrastructure-gold-rush",
        "summary": "This week's biggest story: infrastructure companies building the picks and shovels of AI are raising at record valuations. We break down who's winning and why.",
        "source": "Ben's Bites",
        "source_type": "newsletter",
        "author": "Ben Tossell",
        "score": None,
        "comments_count": None,
        "thumbnail": None,
        "tags": ["bens-bites", "newsletter", "ai"],
    },
    {
        "title": "Apple's AI strategy finally makes sense - and it's different from everyone else's",
        "url": "https://bensbites.beehiiv.com/p/apple-ai-strategy-different",
        "summary": "Apple's on-device AI approach is paying off. Their latest models run entirely on the Neural Engine, offering privacy-first AI that doesn't need cloud compute.",
        "source": "Ben's Bites",
        "source_type": "newsletter",
        "author": "Ben Tossell",
        "score": None,
        "comments_count": None,
        "thumbnail": None,
        "tags": ["bens-bites", "newsletter", "ai"],
    },
    {
        "title": "The best AI tools launched this week (April 1-7, 2026)",
        "url": "https://bensbites.beehiiv.com/p/best-ai-tools-april-2026-week1",
        "summary": "Our weekly roundup of the most interesting AI product launches: a new AI video editor, an autonomous coding agent, and a fascinating AI-powered legal research tool.",
        "source": "Ben's Bites",
        "source_type": "newsletter",
        "author": "Ben Tossell",
        "score": None,
        "comments_count": None,
        "thumbnail": None,
        "tags": ["bens-bites", "newsletter", "ai"],
    },
    # The Rundown AI
    {
        "title": "Microsoft's AI revenue surpasses $30B annually - Copilot adoption drives growth",
        "url": "https://www.therundown.ai/p/microsoft-ai-revenue-30b",
        "summary": "Microsoft reported that AI-driven products now generate over $30 billion in annual revenue, with Copilot for Microsoft 365 adoption growing 300% quarter-over-quarter.",
        "source": "The Rundown AI",
        "source_type": "newsletter",
        "author": "The Rundown AI",
        "score": None,
        "comments_count": None,
        "thumbnail": None,
        "tags": ["rundown-ai", "newsletter", "ai"],
    },
    {
        "title": "AI agents are replacing junior developer roles at major tech companies",
        "url": "https://www.therundown.ai/p/ai-agents-replacing-junior-devs",
        "summary": "A controversial report from McKinsey suggests that AI coding agents are reducing demand for entry-level software engineers by 25-30% at large enterprises.",
        "source": "The Rundown AI",
        "source_type": "newsletter",
        "author": "The Rundown AI",
        "score": None,
        "comments_count": None,
        "thumbnail": None,
        "tags": ["rundown-ai", "newsletter", "ai"],
    },
    {
        "title": "OpenAI and Google in a race to build AI-powered operating systems",
        "url": "https://www.therundown.ai/p/openai-google-ai-operating-systems",
        "summary": "Both companies are reportedly developing AI-native operating systems that could fundamentally change how we interact with computers, moving beyond chat interfaces to ambient AI.",
        "source": "The Rundown AI",
        "source_type": "newsletter",
        "author": "The Rundown AI",
        "score": None,
        "comments_count": None,
        "thumbnail": None,
        "tags": ["rundown-ai", "newsletter", "ai"],
    },
    {
        "title": "The 5-minute AI news: Everything you missed today (April 8)",
        "url": "https://www.therundown.ai/p/5-minute-ai-news-april-8-2026",
        "summary": "Your daily AI digest: NVIDIA announces new inference chips, Stability AI releases SDXL 3.0, China's Baidu claims AGI breakthrough, and more.",
        "source": "The Rundown AI",
        "source_type": "newsletter",
        "author": "The Rundown AI",
        "score": None,
        "comments_count": None,
        "thumbnail": None,
        "tags": ["rundown-ai", "newsletter", "ai"],
    },
]

# Add timestamps (spread across last 24 hours)
for i, article in enumerate(SAMPLE_ARTICLES):
    hours_ago = random.uniform(0.5, 23.5)
    pub_time = now - timedelta(hours=hours_ago)
    article["id"] = make_id(article["url"])
    article["published_at"] = pub_time.isoformat()
    article["scraped_at"] = now.isoformat()

# Sort by published_at descending
SAMPLE_ARTICLES.sort(key=lambda a: a["published_at"], reverse=True)

payload = {
    "last_updated": now.isoformat(),
    "total_articles": len(SAMPLE_ARTICLES),
    "sources_scraped": ["Reddit", "Ben's Bites", "The Rundown AI"],
    "articles": SAMPLE_ARTICLES,
}

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(data_dir, exist_ok=True)

output_path = os.path.join(data_dir, "articles.json")
with open(output_path, "w") as f:
    json.dump(payload, f, indent=2)

print(f"Generated {len(SAMPLE_ARTICLES)} sample articles -> {output_path}")
