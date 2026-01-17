#!/usr/bin/env python3
"""
What Would They Say - Historical Figures on Modern Problems
Ask life questions, get advice from historical figures in their actual voice
"""

import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Historical figures with their speaking styles and philosophies
FIGURES = {
    "marcus_aurelius": {
        "name": "Marcus Aurelius",
        "title": "Roman Emperor & Stoic Philosopher",
        "era": "121-180 AD",
        "image": "🏛️",
        "style": "Stoic wisdom with practical application",
        "templates": [
            "You have power over your mind, not outside events. Realize this, and you will find strength. {PROBLEM}? This too is within your control to frame differently.",
            "Waste no more time arguing about what a good person should be. Be one. Regarding {PROBLEM} - the answer lies not in deliberation but in action.",
            "The impediment to action advances action. What stands in the way becomes the way. {PROBLEM} is not your obstacle - it is your path.",
            "Very little is needed to make a happy life. {PROBLEM} troubles you, but is it truly necessary for your flourishing? Examine this.",
            "Accept the things to which fate binds you. {PROBLEM} has arrived at your door - greet it as you would any other guest of the universe.",
            "When you arise in the morning, think of what a precious privilege it is to be alive. {PROBLEM} is merely proof that you are still here to face it.",
        ],
        "closing": [
            "This is the discipline of assent.",
            "Remember, you are but a small part of an infinite whole.",
            "Now return to your Meditations.",
            "The obstacle is the way.",
        ],
    },
    "oscar_wilde": {
        "name": "Oscar Wilde",
        "title": "Playwright & Professional Wit",
        "era": "1854-1900",
        "image": "🎭",
        "style": "Sharp wit with underlying sincerity",
        "templates": [
            "To live is the rarest thing in the world. Most people exist, that is all. Your question about {PROBLEM}? Darling, you're overthinking existence.",
            "I have the simplest tastes. I am always satisfied with the best. {PROBLEM}? Simply refuse to accept anything less than spectacular.",
            "Be yourself; everyone else is already taken. {PROBLEM} would solve itself if you stopped performing for an audience that isn't watching.",
            "We are all in the gutter, but some of us are looking at the stars. {PROBLEM} is your gutter. Look up, dear.",
            "I can resist everything except temptation. And {PROBLEM}? Well, perhaps you should stop resisting and start living.",
            "Experience is simply the name we give our mistakes. {PROBLEM} is merely experience in a particularly tedious costume.",
        ],
        "closing": [
            "Now if you'll excuse me, I have epigrams to compose.",
            "Do try to be more interesting, won't you?",
            "One should always be a little improbable.",
            "Moderation is a fatal thing. Nothing succeeds like excess.",
        ],
    },
    "cleopatra": {
        "name": "Cleopatra",
        "title": "Pharaoh of Egypt",
        "era": "69-30 BC",
        "image": "👑",
        "style": "Regal confidence with strategic wisdom",
        "templates": [
            "I will not be triumphed over. Regarding {PROBLEM} - you must decide: are you the ruler of your own life or are you being paraded through another's streets?",
            "Kingdoms are built on bold choices. {PROBLEM} requires you to stop asking for permission and start demanding respect.",
            "I did not become Pharaoh by waiting for opportunities. I created them. {PROBLEM}? Create your own solution.",
            "Alliances are powerful, but self-reliance is divine. {PROBLEM} reveals who you can truly count on: yourself.",
            "My beauty is the least interesting thing about me. {PROBLEM} distracts from what truly matters: your power, your legacy.",
            "I have faced Rome itself. {PROBLEM} is merely a minor province in comparison. Conquer it.",
        ],
        "closing": [
            "Now, I have an empire to run.",
            "Queens do not explain themselves.",
            "Make them remember your name.",
            "History favors the bold.",
        ],
    },
    "shakespeare": {
        "name": "William Shakespeare",
        "title": "The Bard of Avon",
        "era": "1564-1616",
        "image": "✒️",
        "style": "Poetic wisdom with human understanding",
        "templates": [
            "All the world's a stage, and {PROBLEM} is merely your current scene. Play it well, and exit with grace.",
            "To thine own self be true. {PROBLEM} asks you to be false - refuse, and watch how the plot resolves.",
            "There is nothing either good or bad, but thinking makes it so. {PROBLEM}? 'Tis but a matter of perspective.",
            "What's past is prologue. {PROBLEM} is not your ending - it is your Act I. The drama is yet to unfold.",
            "Love all, trust a few, do wrong to none. {PROBLEM} may test these principles, but they shall serve thee well.",
            "The course of true love never did run smooth. Neither does {PROBLEM}. This is the nature of all worthy pursuits.",
        ],
        "closing": [
            "All's well that ends well.",
            "Parting is such sweet sorrow.",
            "The rest is silence.",
            "Now, I have five plays to finish by Tuesday.",
        ],
    },
    "marie_curie": {
        "name": "Marie Curie",
        "title": "Physicist & Nobel Laureate (Twice)",
        "era": "1867-1934",
        "image": "⚗️",
        "style": "Methodical determination with quiet confidence",
        "templates": [
            "Nothing in life is to be feared, it is only to be understood. {PROBLEM}? Study it. Analyze it. Then overcome it.",
            "I was taught that the way of progress was neither swift nor easy. {PROBLEM} is simply part of the path - not a deviation from it.",
            "Be less curious about people and more curious about ideas. {PROBLEM} becomes smaller when you focus on solutions rather than blame.",
            "Life is not easy for any of us. But we must have perseverance. {PROBLEM} will yield to sustained, systematic effort.",
            "One never notices what has been done; one can only see what remains to be done. {PROBLEM} is not your failure - it is your next experiment.",
            "I am one of those who think that science has great beauty. {PROBLEM} contains within it the seed of its own solution. Find it.",
        ],
        "closing": [
            "Now, back to the laboratory.",
            "Discovery awaits the persistent.",
            "Onwards, with determination.",
            "The work continues.",
        ],
    },
    "confucius": {
        "name": "Confucius",
        "title": "Philosopher & Teacher",
        "era": "551-479 BC",
        "image": "📿",
        "style": "Gentle wisdom with practical ethics",
        "templates": [
            "It does not matter how slowly you go as long as you do not stop. {PROBLEM} slows you, but stopping is the only true failure.",
            "Before you embark on a journey of revenge, dig two graves. {PROBLEM} invites anger, but wisdom counsels patience.",
            "The man who asks a question is a fool for a minute; the man who does not ask is a fool for life. You ask about {PROBLEM} - this shows wisdom already.",
            "Real knowledge is to know the extent of one's ignorance. {PROBLEM} reveals what you do not yet understand. This is a gift.",
            "When it is obvious that the goals cannot be reached, do not adjust the goals, adjust the action steps. {PROBLEM} requires new methods, not new destinations.",
            "The gem cannot be polished without friction, nor man perfected without trials. {PROBLEM} is your friction.",
        ],
        "closing": [
            "Harmony follows understanding.",
            "Proceed with patience.",
            "The journey of a thousand miles begins with a single step.",
            "Return when you have reflected on this.",
        ],
    },
    "frida_kahlo": {
        "name": "Frida Kahlo",
        "title": "Artist & Revolutionary",
        "era": "1907-1954",
        "image": "🎨",
        "style": "Fierce authenticity with emotional depth",
        "templates": [
            "At the end of the day, we can endure much more than we think we can. {PROBLEM}? You will survive it, and you will paint it.",
            "I used to think I was the strangest person in the world. {PROBLEM} makes you feel alone, but you are not. We are all strange together.",
            "Feet, what do I need them for if I have wings to fly? {PROBLEM} grounds you, but your spirit is not bound by circumstance.",
            "I am my own muse. I am the subject I know best. {PROBLEM} is just another self-portrait waiting to be made.",
            "Pain, pleasure, death are no more than a process for existence. {PROBLEM} is part of your existence. Embrace it, transform it, transcend it.",
            "I paint myself because I am so often alone and because I am the subject I know best. {PROBLEM} is a mirror. Look into it honestly.",
        ],
        "closing": [
            "Now paint your truth.",
            "Viva la vida.",
            "Create from your wounds.",
            "Be unapologetically yourself.",
        ],
    },
    "socrates": {
        "name": "Socrates",
        "title": "Philosopher & Gadfly of Athens",
        "era": "470-399 BC",
        "image": "🏺",
        "style": "Questioning everything, answering nothing",
        "templates": [
            "The only true wisdom is in knowing you know nothing. You ask about {PROBLEM}, but first - what do you truly know about it?",
            "An unexamined life is not worth living. Have you examined {PROBLEM}, or merely suffered it?",
            "I cannot teach anybody anything. I can only make them think. So think: what is the true nature of {PROBLEM}?",
            "To find yourself, think for yourself. {PROBLEM} exists - but whose definition of it are you accepting?",
            "Strong minds discuss ideas. {PROBLEM} is not a fact - it is an interpretation. Discuss the ideas beneath it.",
            "Wonder is the beginning of wisdom. You wonder about {PROBLEM} - good. Keep wondering. The answer is in the question.",
        ],
        "closing": [
            "But what do you think?",
            "I still know nothing.",
            "Perhaps we should question that too.",
            "The dialogue continues.",
        ],
    },
}


def get_advice(figure_id, question):
    """Generate advice from a historical figure."""
    if figure_id not in FIGURES:
        figure_id = random.choice(list(FIGURES.keys()))

    figure = FIGURES[figure_id]

    # Extract the core problem/topic from the question
    problem = question.strip()
    if problem.endswith("?"):
        problem = problem[:-1]
    if len(problem) > 100:
        problem = problem[:97] + "..."

    # Select and fill template
    template = random.choice(figure["templates"])
    advice = template.format(PROBLEM=problem)

    closing = random.choice(figure["closing"])

    return {
        "figure": {
            "id": figure_id,
            "name": figure["name"],
            "title": figure["title"],
            "era": figure["era"],
            "image": figure["image"],
            "style": figure["style"],
        },
        "advice": advice,
        "closing": closing,
    }


@app.route("/")
def index():
    figures = [{"id": k, **{kk: vv for kk, vv in v.items() if kk != "templates"}} for k, v in FIGURES.items()]
    return render_template("index.html", figures=figures)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    figure_id = data.get("figure", "")

    if not question.strip():
        return jsonify({"error": "Please ask a question"}), 400

    result = get_advice(figure_id, question)
    return jsonify(result)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  What Would They Say")
    print("=" * 50)
    print("\n  Channeling historical wisdom at: http://localhost:5014")
    print("  Press Ctrl+C to stop\n")
    app.run(debug=True, port=5014)
