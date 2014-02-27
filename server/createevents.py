from serve import db
from serve import Event

#events = [ 
        #"qigong",
        #"salsa", 
        #"defence",
        #"audi",
        #"cartoon",
        #"dj",
        #"slamdunk",
        #"spikefest",
        #"finearts",
        #"paintball",
        #"hhi",
        #"hogathon",
        #"stuntmania",
        #"warofdjs",
        #"watersports",
        #"hautecouture",
        #"bandish",
        #"pulse",
        #"promenade",
        #"leadingnote",
        #"unplugged",
        #"dhvanik",
        #"lit",
        #"sand",
        #"water",
       #]
events = [
        "litgeneral",
        "litbiztech",
        "litindia",
        "litlitent",
        "litsports",
        "litlonewolf",
        "promenadesolo",
        "promenadedueteastern",
        "promenadeduetwestern"
        ]
eventstoremove = [
        "promenade",
        ]
for event in events:
    e = Event(name=event)
    db.session.add(e)
    db.session.commit()

for event in eventstoremove:
    e = Event.query.filter_by(name=event)
    if e:
        db.session.delete(e)
        db.session.commit()
