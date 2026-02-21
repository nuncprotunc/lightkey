"""
Readability analysis for LightKey index.html
Metrics: Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog,
         SMOG, Coleman-Liau, ARI, Lexical Density, avg sentence/word length
"""
import re, math
from bs4 import BeautifulSoup

# ── 1. Extract visible text from HTML ─────────────────────────────────────────
with open('/Users/jsp/lightkey/index.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
for tag in soup(['script', 'style', 'svg', 'noscript', 'head']):
    tag.decompose()

raw = soup.get_text(separator=' ')
text = re.sub(r'\s+', ' ', raw).strip()

# ── 2. Tokenise ───────────────────────────────────────────────────────────────
# Sentences: split on . ! ? followed by space/end
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text)
             if len(re.findall(r"[a-zA-Z']+", s)) >= 3]
if not sentences:
    # fallback: split on any period/!/?
    sentences = [s.strip() for s in re.split(r'[.!?]+', text)
                 if len(re.findall(r"[a-zA-Z']+", s)) >= 3]
# Words: alphabetic tokens only
words = re.findall(r"[a-zA-Z']+", text)
# Syllable counter (English approximation)
def syllables(word):
    word = word.lower().strip("'")
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^aeiou])es$', '', word)
    word = re.sub(r'(?:[^aeiou])ed$', '', word)
    word = re.sub(r'e$', '', word)
    count = len(re.findall(r'[aeiou]+', word))
    return max(1, count)

syl_counts = [syllables(w) for w in words]
total_syllables = sum(syl_counts)
total_words     = len(words)
total_sentences = len(sentences)
total_chars     = sum(len(w) for w in words)

# ── 3. Metrics ────────────────────────────────────────────────────────────────
asl  = total_words / total_sentences          # avg sentence length
asw  = total_syllables / total_words          # avg syllables per word
acw  = total_chars / total_words              # avg chars per word

# Flesch Reading Ease (higher = easier; 60-70 = standard)
fre  = 206.835 - 1.015 * asl - 84.6 * asw

# Flesch-Kincaid Grade Level
fkg  = 0.39 * asl + 11.8 * asw - 15.59

# Gunning Fog Index
complex_words = sum(1 for c in syl_counts if c >= 3)
fog  = 0.4 * (asl + 100 * complex_words / total_words)

# SMOG (requires ≥30 sentences; approximation below that)
smog = 3 + math.sqrt(complex_words * (30 / total_sentences)) if total_sentences >= 3 else None

# Coleman-Liau Index
cli  = 0.0588 * (total_chars / total_words * 100) - 0.296 * (total_sentences / total_words * 100) - 15.8

# Automated Readability Index
ari  = 4.71 * acw + 0.5 * asl - 21.43

# Lexical Density = unique content words / total words
unique_words = set(w.lower() for w in words)
lex_density  = len(unique_words) / total_words * 100

# ── 4. Report ─────────────────────────────────────────────────────────────────
print(f"{'='*54}")
print(f"  LightKey index.html — Readability Report")
print(f"{'='*54}")
print(f"  Words:              {total_words:>6}")
print(f"  Sentences:          {total_sentences:>6}")
print(f"  Syllables:          {total_syllables:>6}")
print(f"  Unique words:       {len(unique_words):>6}")
print(f"{'─'*54}")
print(f"  Avg sentence length:{asl:>7.1f} words")
print(f"  Avg word length:    {acw:>7.2f} chars")
print(f"  Avg syllables/word: {asw:>7.2f}")
print(f"{'─'*54}")
print(f"  Flesch Reading Ease:{fre:>7.1f}  (60-70 = plain English)")
print(f"  Flesch-Kincaid Grade:{fkg:>6.1f}  (US school grade)")
print(f"  Gunning Fog Index:  {fog:>7.1f}  (12 = high school)")
if smog:
    print(f"  SMOG Grade:         {smog:>7.1f}  (years of education)")
print(f"  Coleman-Liau Index: {cli:>7.1f}  (US school grade)")
print(f"  Auto Readability:   {ari:>7.1f}  (US school grade)")
print(f"{'─'*54}")
print(f"  Lexical Density:    {lex_density:>7.1f}%  (40-60% = informational)")
print(f"{'='*54}")

# ── 5. Interpretation ─────────────────────────────────────────────────────────
grade = (fkg + fog + cli + ari) / 4
print(f"\n  Avg grade level (4-metric): {grade:.1f}")
if fre >= 70:
    ease = "Easy — accessible to most readers"
elif fre >= 60:
    ease = "Standard — plain English range"
elif fre >= 50:
    ease = "Fairly difficult — some college"
elif fre >= 30:
    ease = "Difficult — college level"
else:
    ease = "Very difficult — professional/academic"
print(f"  Reading ease verdict:       {ease}")
print()
