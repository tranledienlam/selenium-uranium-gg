import time
import random
import inspect
import requests
import re
from pathlib import Path
from typing import List
from io import BytesIO
import google.generativeai as genai
from PIL import Image

BIP39_WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual", "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance", "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent", "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among", "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry", "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique", "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april", "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor", "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact", "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction", "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid", "awake", "aware", "away", "awesome", "awful", "awkward", "axis", "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball", "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base", "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become", "beef", "before", "begin", "behave", "behind", "believe", "below", "belt", "bench", "benefit", "best", "betray", "better", "between", "beyond", "bicycle", "bid", "bike", "bind", "biology", "bird", "birth", "bitter", "black", "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood", "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body", "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring", "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket", "brain", "brand", "brass", "brave", "bread", "breeze", "brick", "bridge", "brief", "bright", "bring", "brisk", "broccoli", "broken", "bronze", "broom", "brother", "brown", "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb", "bulk", "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus", "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable", "cactus", "cage", "cake", "call", "calm", "camera", "camp", "can", "canal", "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital", "captain", "car", "carbon", "card", "cargo", "carpet", "carry", "cart", "case", "cash", "casino", "castle", "casual", "cat", "catalog", "catch", "category", "cattle", "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census", "century", "cereal", "certain", "chair", "chalk", "champion", "change", "chaos", "chapter", "charge", "chase", "chat", "cheap", "check", "cheese", "chef", "cherry", "chest", "chicken", "chief", "child", "chimney", "choice", "choose", "chronic", "chuckle", "chunk", "churn", "cigar", "cinnamon", "circle", "citizen", "city", "civil", "claim", "clap", "clarify", "claw", "clay", "clean", "clerk", "clever", "click", "client", "cliff", "climb", "clinic", "clip", "clock", "clog", "close", "cloth", "cloud", "clown", "club", "clump", "cluster", "clutch", "coach", "coast", "coconut", "code", "coffee", "coil", "coin", "collect", "color", "column", "combine", "come", "comfort", "comic", "common", "company", "concert", "conduct", "confirm", "congress", "connect", "consider", "control", "convince", "cook", "cool", "copper", "copy", "coral", "core", "corn", "correct", "cost", "cotton", "couch", "country", "couple", "course", "cousin", "cover", "coyote", "crack", "cradle", "craft", "cram", "crane", "crash", "crater", "crawl", "crazy", "cream", "credit", "creek", "crew", "cricket", "crime", "crisp", "critic", "crop", "cross", "crouch", "crowd", "crucial", "cruel", "cruise", "crumble", "crunch", "crush", "cry", "crystal", "cube", "culture", "cup", "cupboard", "curious", "current", "curtain", "curve", "cushion", "custom", "cute", "cycle", "dad", "damage", "damp", "dance", "danger", "daring", "dash", "daughter", "dawn", "day", "deal", "debate", "debris", "decade", "december", "decide", "decline", "decorate", "decrease", "deer", "defense", "define", "defy", "degree", "delay", "deliver", "demand", "demise", "denial", "dentist", "deny", "depart", "depend", "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk", "despair", "destroy", "detail", "detect", "develop", "device", "devote", "diagram", "dial", "diamond", "diary", "dice", "diesel", "diet", "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur", "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss", "disorder", "display", "distance", "divert", "divide", "divorce", "dizzy", "doctor", "document", "dog", "doll", "dolphin", "domain", "donate", "donkey", "donor", "door", "dose", "double", "dove", "draft", "dragon", "drama", "drastic", "draw", "dream", "dress", "drift", "drill", "drink", "drip", "drive", "drop", "drum", "dry", "duck", "dumb", "dune", "during", "dust", "dutch", "duty", "dwarf", "dynamic", "eager", "eagle", "early", "earn", "earth", "easily", "east", "easy", "echo", "ecology", "economy", "edge", "edit", "educate", "effort", "egg", "eight", "either", "elbow", "elder", "electric", "elegant", "element", "elephant", "elevator", "elite", "else", "embark", "embody", "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable", "enact", "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine", "enhance", "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter", "entire", "entry", "envelope", "episode", "equal", "equip", "era", "erase", "erode", "erosion", "error", "erupt", "escape", "essay", "essence", "estate", "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact", "example", "excess", "exchange", "excite", "exclude", "excuse", "execute", "exercise", "exhaust", "exhibit", "exile", "exist", "exit", "exotic", "expand", "expect", "expire", "explain", "expose", "express", "extend", "extra", "eye", "eyebrow", "fabric", "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame", "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat", "fatal", "father", "fatigue", "fault", "favorite", "feature", "february", "federal", "fee", "feed", "feel", "female", "fence", "festival", "fetch", "fever", "few", "fiber", "fiction", "field", "figure", "file", "film", "filter", "final", "find", "fine", "finger", "finish", "fire", "firm", "first", "fiscal", "fish", "fit", "fitness", "fix", "flag", "flame", "flash", "flat", "flavor", "flee", "flight", "flip", "float", "flock", "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog", "foil", "fold", "follow", "food", "foot", "force", "forest", "forget", "fork", "fortune", "forum", "forward", "fossil", "foster", "found", "fox", "fragile", "frame", "frequent", "fresh", "friend", "fringe", "frog", "front", "frost", "frown", "frozen", "fruit", "fuel", "fun", "funny", "furnace", "fury", "future", "gadget", "gain", "galaxy", "gallery", "game", "gap", "garage", "garbage", "garden", "garlic", "garment", "gas", "gasp", "gate", "gather", "gauge", "gaze", "general", "genius", "genre", "gentle", "genuine", "gesture", "ghost", "giant", "gift", "giggle", "ginger", "giraffe", "girl", "give", "glad", "glance", "glare", "glass", "glide", "glimpse", "globe", "gloom", "glory", "glove", "glow", "glue", "goat", "goddess", "gold", "good", "goose", "gorilla", "gospel", "gossip", "govern", "gown", "grab", "grace", "grain", "grant", "grape", "grass", "gravity", "great", "green", "grid", "grief", "grit", "grocery", "group", "grow", "grunt", "guard", "guess", "guide", "guilt", "guitar", "gun", "gym", "habit", "hair", "half", "hammer", "hamster", "hand", "happy", "harbor", "hard", "harsh", "harvest", "hat", "have", "hawk", "hazard", "head", "health", "heart", "heavy", "hedgehog", "height", "hello", "helmet", "help", "hen", "hero", "hidden", "high", "hill", "hint", "hip", "hire", "history", "hobby", "hockey", "hold", "hole", "holiday", "hollow", "home", "honey", "hood", "hope", "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover", "hub", "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry", "hurt", "husband", "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore", "ill", "illegal", "illness", "image", "imitate", "immense", "immune", "impact", "impose", "improve", "impulse", "inch", "include", "income", "increase", "index", "indicate", "indoor", "industry", "infant", "inflict", "inform", "inhale", "inherit", "initial", "inject", "injury", "inmate", "inner", "innocent", "input", "inquiry", "insane", "insect", "inside", "inspire", "install", "intact", "interest", "into", "invest", "invite", "involve", "iron", "island", "isolate", "issue", "item", "ivory", "jacket", "jaguar", "jar", "jazz", "jealous", "jeans", "jelly", "jewel", "job", "join", "joke", "journey", "joy", "judge", "juice", "jump", "jungle", "junior", "junk", "just", "kangaroo", "keen", "keep", "ketchup", "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit", "kitchen", "kite", "kitten", "kiwi", "knee", "knife", "knock", "know", "lab", "label", "labor", "ladder", "lady", "lake", "lamp", "language", "laptop", "large", "later", "latin", "laugh", "laundry", "lava", "law", "lawn", "lawsuit", "layer", "lazy", "leader", "leaf", "learn", "leave", "lecture", "left", "leg", "legal", "legend", "leisure", "lemon", "lend", "length", "lens", "leopard", "lesson", "letter", "level", "liar", "liberty", "library", "license", "life", "lift", "light", "like", "limb", "limit", "link", "lion", "liquid", "list", "little", "live", "lizard", "load", "loan", "lobster", "local", "lock", "logic", "lonely", "long", "loop", "lottery", "loud", "lounge", "love", "loyal", "lucky", "luggage", "lumber", "lunar", "lunch", "luxury", "lyrics", "machine", "mad", "magic", "magnet", "maid", "mail", "main", "major", "make", "mammal", "man", "manage", "mandate", "mango", "mansion", "manual", "maple", "marble", "march", "margin", "marine", "market", "marriage", "mask", "mass", "master", "match", "material", "math", "matrix", "matter", "maximum", "maze", "meadow", "mean", "measure", "meat", "mechanic", "medal", "media", "melody", "melt", "member", "memory", "mention", "menu", "mercy", "merge", "merit", "merry", "mesh", "message", "metal", "method", "middle", "midnight", "milk", "million", "mimic", "mind", "minimum", "minor", "minute", "miracle", "mirror", "misery", "miss", "mistake", "mix", "mixed", "mixture", "mobile", "model", "modify", "mom", "moment", "monitor", "monkey", "monster", "month", "moon", "moral", "more", "morning", "mosquito", "mother", "motion", "motor", "mountain", "mouse", "move", "movie", "much", "muffin", "mule", "multiply", "muscle", "museum", "mushroom", "music", "must", "mutual", "myself", "mystery", "myth", "naive", "name", "napkin", "narrow", "nasty", "nation", "nature", "near", "neck", "need", "negative", "neglect", "neither", "nephew", "nerve", "nest", "net", "network", "neutral", "never", "news", "next", "nice", "night", "noble", "noise", "nominee", "noodle", "normal", "north", "nose", "notable", "note", "nothing", "notice", "novel", "now", "nuclear", "number", "nurse", "nut", "oak", "obey", "object", "oblige", "obscure", "observe", "obtain", "obvious", "occur", "ocean", "october", "odor", "off", "offer", "office", "often", "oil", "okay", "old", "olive", "olympic", "omit", "once", "one", "onion", "online", "only", "open", "opera", "opinion", "oppose", "option", "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient", "original", "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside", "oval", "oven", "over", "own", "owner", "oxygen", "oyster", "ozone", "pact", "paddle", "page", "pair", "palace", "palm", "panda", "panel", "panic", "panther", "paper", "parade", "parent", "park", "parrot", "party", "pass", "patch", "path", "patient", "patrol", "pattern", "pause", "pave", "payment", "peace", "peanut", "pear", "peasant", "pelican", "pen", "penalty", "pencil", "people", "pepper", "perfect", "permit", "person", "pet", "phone", "photo", "phrase", "physical", "piano", "picnic", "picture", "piece", "pig", "pigeon", "pill", "pilot", "pink", "pioneer", "pipe", "pistol", "pitch", "pizza", "place", "planet", "plastic", "plate", "play", "please", "pledge", "pluck", "plug", "plunge", "poem", "poet", "point", "polar", "pole", "police", "pond", "pony", "pool", "popular", "portion", "position", "possible", "post", "potato", "pottery", "poverty", "powder", "power", "practice", "praise", "predict", "prefer", "prepare", "present", "pretty", "prevent", "price", "pride", "primary", "print", "priority", "prison", "private", "prize", "problem", "process", "produce", "profit", "program", "project", "promote", "proof", "property", "prosper", "protect", "proud", "provide", "public", "pudding", "pull", "pulp", "pulse", "pumpkin", "punch", "pupil", "puppy", "purchase", "purity", "purpose", "purse", "push", "put", "puzzle", "pyramid", "quality", "quantum", "quarter", "question", "quick", "quit", "quiz", "quote", "rabbit", "raccoon", "race", "rack", "radar", "radio", "rail", "rain", "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare", "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason", "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce", "reflect", "reform", "refuse", "region", "regret", "regular", "reject", "relax", "release", "relief", "rely", "remain", "remember", "remind", "remove", "render", "renew", "rent", "reopen", "repair", "repeat", "replace", "report", "require", "rescue", "resemble", "resist", "resource", "response", "result", "retire", "retreat", "return", "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon", "rice", "rich", "ride", "ridge", "rifle", "right", "rigid", "ring", "riot", "ripple", "risk", "ritual", "rival", "river", "road", "roast", "robot", "robust", "rocket", "romance", "roof", "rookie", "room", "rose", "rotate", "rough", "round", "route", "royal", "rubber", "rude", "rug", "rule", "run", "runway", "rural", "sad", "saddle", "sadness", "safe", "sail", "salad", "salmon", "salon", "salt", "salute", "same", "sample", "sand", "satisfy", "satoshi", "sauce", "sausage", "save", "say", "scale", "scan", "scare", "scatter", "scene", "scheme", "school", "science", "scissors", "scorpion", "scout", "scrap", "screen", "script", "scrub", "sea", "search", "season", "seat", "second", "secret", "section", "security", "seed", "seek", "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series", "service", "session", "settle", "setup", "seven", "shadow", "shaft", "shallow", "share", "shed", "shell", "sheriff", "shield", "shift", "shine", "ship", "shiver", "shock", "shoe", "shoot", "shop", "short", "shoulder", "shove", "shrimp", "shrug", "shuffle", "shy", "sibling", "sick", "side", "siege", "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple", "since", "sing", "siren", "sister", "situate", "six", "size", "skate", "sketch", "ski", "skill", "skin", "skirt", "skull", "slab", "slam", "sleep", "slender", "slice", "slide", "slight", "slim", "slogan", "slot", "slow", "slush", "small", "smart", "smile", "smoke", "smooth", "snack", "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock", "soda", "soft", "solar", "soldier", "solid", "solution", "solve", "someone", "song", "soon", "sorry", "sort", "soul", "sound", "soup", "source", "south", "space", "spare", "spatial", "spawn", "speak", "special", "speed", "spell", "spend", "sphere", "spice", "spider", "spike", "spin", "spirit", "split", "spoil", "sponsor", "spoon", "sport", "spot", "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel", "stable", "stadium", "staff", "stage", "stairs", "stamp", "stand", "start", "state", "stay", "steak", "steel", "stem", "step", "stereo", "stick", "still", "sting", "stock", "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike", "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit", "subway", "success", "such", "sudden", "suffer", "sugar", "suggest", "suit", "summer", "sun", "sunny", "sunset", "super", "supply", "supreme", "sure", "surface", "surge", "surprise", "surround", "survey", "suspect", "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet", "swift", "swim", "swing", "switch", "sword", "symbol", "symptom", "syrup", "system", "table", "tackle", "tag", "tail", "talent", "talk", "tank", "tape", "target", "task", "taste", "tattoo", "taxi", "teach", "team", "tell", "ten", "tenant", "tennis", "tent", "term", "test", "text", "thank", "that", "theme", "then", "theory", "there", "they", "thing", "this", "thought", "three", "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber", "time", "tiny", "tip", "tired", "tissue", "title", "toast", "tobacco", "today", "toddler", "toe", "together", "toilet", "token", "tomato", "tomorrow", "tone", "tongue", "tonight", "tool", "tooth", "top", "topic", "topple", "torch", "tornado", "tortoise", "toss", "total", "tourist", "toward", "tower", "town", "toy", "track", "trade", "traffic", "tragic", "train", "transfer", "trap", "trash", "travel", "tray", "treat", "tree", "trend", "trial", "tribe", "trick", "trigger", "trim", "trip", "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust", "truth", "try", "tube", "tuition", "tumble", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve", "twenty", "twice", "twin", "twist", "two", "type", "typical", "ugly", "umbrella", "unable", "unaware", "uncle", "uncover", "under", "undo", "unfair", "unfold", "unhappy", "uniform", "unique", "unit", "universe", "unknown", "unlock", "until", "unusual", "unveil", "update", "upgrade", "uphold", "upon", "upper", "upset", "urban", "urge", "usage", "use", "used", "useful", "useless", "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve", "van", "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet", "vendor", "venture", "venue", "verb", "verify", "version", "very", "vessel", "veteran", "viable", "vibrant", "vicious", "victory", "video", "view", "village", "vintage", "violin", "virtual", "virus", "visa", "visit", "visual", "vital", "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage", "wage", "wagon", "wait", "walk", "wall", "walnut", "want", "warfare", "warm", "warrior", "wash", "wasp", "waste", "water", "wave", "way", "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding", "weekend", "weird", "welcome", "west", "wet", "whale", "what", "wheat", "wheel", "when", "where", "whip", "whisper", "wide", "width", "wife", "wild", "will", "win", "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom", "wise", "wish", "witness", "wolf", "woman", "wonder", "wood", "wool", "word", "work", "world", "worry", "worth", "wrap", "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year", "yellow", "you", "young", "youth", "zebra", "zero", "zone", "zoo"
]

class SeedConverter:
    @staticmethod
    def _seed_to_indices(seed: List[str]) -> List[int]:
        """
        Chuyển danh sách từ seed thành danh sách chỉ số tương ứng.
        """

        return [BIP39_WORDLIST.index(word) for word in seed]

    @staticmethod
    def _indices_to_seed(indices: List[int]) -> List[str]:
        """
        Chuyển danh sách chỉ số thành danh sách từ seed tương ứng.
        """
        return [BIP39_WORDLIST[index] for index in indices]

    @staticmethod
    def _transform_indices(indices: List[int], key: int) -> List[int]:
        """
        Biến đổi danh sách chỉ số bằng cách sử dụng khóa (key).
        """
        return [(index + key) % len(BIP39_WORDLIST) for index in indices]

    @staticmethod
    def encrypt(seed: str, key: int = 42):
        """
        Chuyển đổi seed gốc thành seed khác dựa trên khóa (key).

        Args:
            seed (str): Chuỗi seed gốc (12 từ cách nhau bởi dấu cách).
            key (int): Khóa để mã hóa seed.

        Returns:
            str: Chuỗi seed mới (12 từ cách nhau bởi dấu cách).
        """
        seed_words = seed.split(" ")
        
        seed_indices = SeedConverter._seed_to_indices(seed_words)
        transformed_indices = SeedConverter._transform_indices(
            seed_indices, key)
        encrypt_words = SeedConverter._indices_to_seed(transformed_indices)
        return " ".join(encrypt_words)

    @staticmethod
    def decrypt(encrypted_seed: str, key: int = 42) -> str:
        """
        Chuyển đổi seed khác về seed gốc dựa trên khóa (key).

        Args:
            encrypted_seed (List[str]): Danh sách 12 từ seed đã mã hóa.
            key (int): Khóa để giải mã seed.

        Returns:
            str: Chuỗi seed gốc (12 từ cách nhau bởi dấu cách).
        """
        seed_words = encrypted_seed.split(" ")
        seed_indices = SeedConverter._seed_to_indices(seed_words)
        original_indices = SeedConverter._transform_indices(seed_indices, -key)
        original_seed = SeedConverter._indices_to_seed(original_indices)
        return " ".join(original_seed)


class Utility:
    @staticmethod
    def wait_time(second: int = 5, fix: bool = False) -> True:
        '''
        Đợi trong một khoảng thời gian nhất định.  Với giá trị dao động từ -50% đên 50%

        Args:
            seconds (int) = 2: Số giây cần đợi.
            fix (bool) = False: False sẽ random, True không random
        '''
        if not fix:
            gap = 0.4
            second = random.uniform(second * (1 - gap), second * (1 + gap))

        time.sleep(second)
        return True
    
    @staticmethod
    def logger(profile_name: str = 'System', message: str = 'Chưa có mô tả nhật ký', show_log: bool = True):
        '''
        Ghi và hiển thị thông báo nhật ký (log)
        
        Cấu trúc log hiển thị:
            [profile_name][func_thuc_thi]: {message}
        
        Args:
            profile_name (str): tên hồ sơ hiện tại
            message (str): Nội dung thông báo log.
            show_log (bool, option): cho phép hiển thị nhật ký hay không. Mặc định: True (cho phép)
        '''
        if show_log:
            func_name = inspect.stack()[2].function
            print(f'[{profile_name}][{func_name}]: {message}')

    @staticmethod
    def get_telegram_credentials():
        """
        Lấy thông tin token Telegram và chat ID từ tệp cấu hình.

        Tệp cấu hình `token.txt` phải nằm trong cùng thư mục với tệp mã nguồn, 
        và nội dung tệp phải có định dạng: `chat_id|telegram_token`.

        Returns:
            tuple: Gồm hai phần tử (chat_id, telegram_token) nếu tệp tồn tại và hợp lệ.
            None: Nếu tệp không tồn tại hoặc nội dung không hợp lệ.

        Ghi chú:
            - Nếu tệp không tồn tại, sẽ ghi log thông báo và trả về None.
            - Nếu nội dung tệp không hợp lệ (không chứa ký tự `|`), sẽ trả về None.
        """
        config_path = Path(__file__).parent / 'token.txt'

        if config_path.exists():
            try:
                with open(config_path, 'r') as file:
                    data = file.readlines()
                for line in data:
                    if line.strip().startswith('tele_bot'):
                        parts = [part.strip() for part in line.strip().split('|')]
                        if len(parts) >= 3:
                            # return chat_id, telegram_token
                            return parts[1], parts[2]
                        else:
                            Utility.logger(
                                message=f'Nội dung tệp {config_path} không hợp lệ. Định dạng phải là "tele_bot|[chat_id]|[telegram_token]".')
                            continue
                        
                Utility.logger(
                    message=f'Tệp {config_path} không tồn tại "tele_bot|[chat_id]|[telegram_token]". Hình ảnh sẽ được lưu vào thư mục "snapshot".')
                return None
            
            except Exception as e:
                Utility.logger(message=f'Lỗi khi đọc tệp {config_path}: {e}')
                return None
        else:
            Utility.logger(
                message=f'Tệp {config_path} không tồn tại. Hình ảnh sẽ được lưu vào thư mục "snapshot".')
            return None
        
    @staticmethod
    def is_proxy_working(proxy_info: str = None):
        ''' Kiểm tra proxy có hoạt động không bằng cách gửi request đến một trang kiểm tra IP
        
        Args:
            proxy_info (str, option): thông tin proxy được truyền vào có dạng sau
                - "ip:port"
                - "username:password@ip:port"
        
        Returns:
            bool: True nếu proxy hoạt động, False nếu không.
        '''
        if not proxy_info:
            return False
        
        proxies = {
            "http": f"http://{proxy_info}",
            "https": f"https://{proxy_info}",
        }
        
        test_url = "http://ip-api.com/json"  # API kiểm tra địa chỉ IP

        try:
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"✅ Proxy hoạt động! IP: {response.json().get('query')}")
                return True
            else:
                print(f"❌ Proxy {proxy_info} không hoạt động! Mã lỗi: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Proxy {proxy_info} lỗi: {e}")
            return False
    
    @staticmethod
    def get_data(*field_names):
        '''
        Lấy dữ liệu từ tệp data.txt

        Args:
            *field_names: tên các trường cần lấy

        Returns:
            list: danh sách các dictionary, mỗi dictionary là một profile

        Xử lý dữ liệu:
            - Nếu parts trong dòng ít hơn field_names, field_name được gán bằng None
            - Nếu parts trong dòng nhiều hơn field_names, phần tử còn lại sẽ được gán vào `extra_fields`
            - Dữ liệu phải bắt đầu bằng `profile_name`, kết thúc bằng `extra_fields` (optional) và `proxy_info` (optional)
        '''
        DATA_DIR = Path(__file__).parent/'data.txt'

        if not DATA_DIR.exists():
            print(f"File {DATA_DIR} không tồn tại.")
            return []

        proxy_re = re.compile(r"^(?:\w+:\w+@)?\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}$")
        profiles = []

        with open(DATA_DIR, 'r') as file:
            data = file.readlines()

        for line in data:
            parts = [part.strip() for part in line.strip().split('|')]
            
            # Kiểm tra và tách proxy nếu có
            proxy_info = parts[-1] if proxy_re.match(parts[-1]) else None
            if proxy_info:
                parts = parts[:-1]
                
            # Kiểm tra số lượng dữ liệu
            if len(parts) < 1:
                print(f"Warning: Dữ liệu không hợp lệ - {line}")
                continue
                
            # Tạo dictionary với các trường được chỉ định
            profile = {}
            # Gán giá trị cho các field có trong parts
            for i, field_name in enumerate(field_names):
                if i < len(parts):
                    profile[field_name] = parts[i]
                else:
                    profile[field_name] = None

            profile['extra_fields'] = parts[len(field_names):]
            profile['proxy_info'] = proxy_info
            profiles.append(profile)
        
        return profiles
    
    @staticmethod
    def fake_data(field_name: str = "profile_name", numbers: int = 0):
        profiles = []
        for i in range(numbers):
            profile = {}
            profile[field_name] = str(i + 1)
            profiles.append(profile)
        return profiles


class AIHelper:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Khởi tạo AI Helper với API key và model name
        
        Args:
            api_key (str): API key của Gemini
            model_name (str, optional): Tên model sử dụng. Mặc định là "gemini-2.0-flash"
            
        Returns:
            bool: True nếu AI hoạt động, False nếu không hoạt động
        """
        self.is_working = False
        token = self.get_token()
        if token:
            try:
                genai.configure(api_key=token)
                self.model = genai.GenerativeModel(model_name)
                test_ai = self.ask(prompt="Hello, world!. Only reply with 1 word.")
                text, error = test_ai
                if text:
                    self.is_working = True
                else:
                    Utility.logger(message=f'Lỗi khi gửi yêu cầu đến AI - {error}')
                    self.is_working = False
            except Exception as e:
                Utility.logger(message=f'Lỗi khi khởi tạo AI - {str(e)}')
                self.is_working = False
        else:
            self.is_working = False

    def get_token(self):
        config_path = Path(__file__).parent / 'token.txt'

        if config_path.exists():
            try:
                with open(config_path, 'r') as file:
                    data = file.readlines()
                for line in data:
                    if line.strip().startswith('ai_bot'):
                        parts = [part.strip() for part in line.strip().split('|')]
                        if len(parts) >= 2:
                            # return token
                            return parts[1]
                        else:
                            Utility.logger(
                                message=f'Nội dung tệp {config_path} không hợp lệ. Định dạng phải là "ai_bot|[token]".')
                            continue
                        
                Utility.logger(
                    message=f'Tệp {config_path} không tồn tại "ai_bot|[token]". Sẽ không thể sử dụng bot AI.')
                return None
            
            except Exception as e:
                Utility.logger(message=f'Lỗi khi đọc tệp {config_path}: {e}')
                return None
        else:
            Utility.logger(
                message=f'Tệp {config_path} không tồn tại. Sẽ không thể sử dụng bot AI.')
            return None

    def process_image(self, image: Image) -> Image:
        """
        Xử lý ảnh để tối ưu kích thước trước khi gửi lên AI
        
        Args:
            image (Image): Ảnh cần xử lý
            
        Returns:
            Image: Ảnh đã được resize
        """
        if type(image) == bytes:
            image = Image.open(BytesIO(image))
            
        width, height = image.size
        max_size = 384
        
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        new_size = (new_width, new_height)
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def ask(self, prompt: str, image: Image = None) -> tuple[str | None, str | None]:
        """
        Gửi prompt và ảnh lên AI để phân tích
        
        Args:
            prompt (str): Câu hỏi hoặc yêu cầu gửi đến AI
            image (Image, optional): Ảnh cần phân tích. Nếu None, sẽ trả về None
            
        Returns:
            tuple[str | None, str | None]: 
                - Phần tử đầu tiên: Kết quả phân tích từ AI hoặc None nếu có lỗi
                - Phần tử thứ hai: Thông báo lỗi hoặc None nếu không có lỗi
        """
        try:
            if image:
                resized_image = self.process_image(image)
                response = self.model.generate_content([prompt, resized_image])
            else:
                response = self.model.generate_content([prompt])
            
            return response.text, None
            
        except Exception as e:
            error_message = str(e)
            if "API_KEY_INVALID" in error_message or "API key not valid" in error_message:
                return None, f"API key không hợp lệ. Vui lòng kiểm tra lại token."
            elif "blocked" in error_message.lower():
                return None, f"Prompt vi phạm chính sách nội dung - {error_message}"
            elif "permission" in error_message.lower():
                return None, f"Không có quyền truy cập API - {error_message}"
            elif "quota" in error_message.lower() or "limit" in error_message.lower():
                return None, f"Vượt quá giới hạn tài nguyên - {error_message}"
            elif "timeout" in error_message.lower() or "deadline" in error_message.lower():
                return None, f"Vượt quá thời gian xử lý - {error_message}"
            else:
                return None, f"Lỗi không xác định khi gửi yêu cầu đến AI - {error_message}"
        
if __name__ == "__main__":
    profiles = Utility.get_data('profile_name', 'pass', 'seeds')
    print(profiles)
    # Seed ban đầu
    # original_seed = "gas vacuum social float present exist atom gold relax glance credit soldier"
    # key = 42  # Khóa để chuyển đổi

    # # Chuyển đổi seed gốc thành seed khác
    # encrypted_seed = SeedConverter.encrypt(original_seed, key)

    # # Chuyển đổi seed khác về seed gốc
    # decrypted_seed = SeedConverter.decrypt(encrypted_seed, key)

    # # Kiểm tra kết quả
    # assert original_seed == decrypted_seed, "Seed sau giải mã không khớp với seed gốc!"
