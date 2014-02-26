from serve import db
from serve import Event

events = [ 
        "qigong",
        "salsa", 
        "defence",
        "audi",
        "cartoon",
        "dj",
        "slamdunk",
        "spikefest",
        "finearts",
        "paintball",
        "hhi",
        "hogathon",
        "stuntmania",
        "warofdjs",
        "watersports",
        "hautecoutre",
        "bandish",
        "pulse",
        "promenade",
        "leadingnote",
        "unplugged",
        "dhvanik",
        "lit",
        "sand",
        "water",
       ]
for event in events:
    e = Event(name=event)
    db.session.add(e)
    db.session.commit()

        
        
