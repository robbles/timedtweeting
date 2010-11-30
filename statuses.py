from jinja2 import Template
from random import randint

templates = [
    #Template("""@{{ screen_name }} has spent {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets!"""),
    #Template("""@{{ screen_name }} has {{ statuses_count }} tweets, which took about {{ time_tweeting|round(1) }} hours to write!"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have eaten {{ (time_tweeting/2)|int }} candy bars"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have roasted {{ (time_tweeting/4)|int }} turkeys"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have built {{ (time_tweeting/2)|int }} epic sandcastles"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have visited reddit.com {{ (time_tweeting*2.7)|int }} times"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have played {{ (time_tweeting/2.5)|int }} games of ice hockey"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have wrestled {{ (time_tweeting/6)|int }} bears"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have baked {{ (time_tweeting/3)|int }} pizzas"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have climbed Mt. Everest {{ (time_tweeting/21)|round(1) }} times"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have biked across Canada {{ (time_tweeting/653.5)|round(1) }} times"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have beaten Halo: Reach {{ (time_tweeting/10)|int }} times"""),

    Template("""@{{ screen_name }} has spent about {{ time_tweeting|round(1) }} hours writing {{ statuses_count }} tweets. In that time, they could have flown to the Moon {{ (time_tweeting/76)|round(1) }} times"""),
]

# User based on worst imaginable scenario
sample_user = {'statuses_count': 130243, 'screen_name': u'abcdefghiklmnop', 'time_tweeting': 2200.71666666666667}

def render_status_n(user, num=0):
    template = templates[num % len(templates)]
    return template.render(user)

def render_random_status(user):
    template = templates[randint(0, len(templates)-1)]
    return template.render(user)

def test_statuses():
    for template in templates:
        status = template.render(sample_user)
        print "%d : \"%s\"" % (len(status), status)
        print



