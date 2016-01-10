from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=128)
    short = models.CharField(max_length=20)

class Game(models.Model):
    gid = models.CharField(max_length=30)
    date = models.DateField()
    home_team = models.ForeignKey(Team, related_name="home_team_game")
    away_team = models.ForeignKey(Team, related_name="away_team_game")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

class Atbat(models.Model):

    delete_blanks = [
        'start_tfs',
        'start_tfs_zulu',
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    inning = models.IntegerField(blank=True, null=True)
    top_bottom = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    b = models.IntegerField(blank=True, null=True)
    s = models.IntegerField(blank=True, null=True)
    o = models.IntegerField(blank=True, null=True)
    start_tfs = models.IntegerField(blank=True, null=True)
    start_tfs_zulu = models.DateTimeField(blank=True, null=True)
    batter = models.IntegerField(blank=True, null=True)
    stand = models.CharField(max_length=3, blank=True, null=True)
    b_height = models.CharField(max_length=10, blank=True, null=True)
    pitcher = models.IntegerField(blank=True, null=True)
    p_throws = models.CharField(max_length=3, blank=True, null=True)
    des = models.CharField(max_length=1028, blank=True, null=True)
    des_es = models.CharField(max_length=1028, blank=True, null=True)
    event_num = models.IntegerField(blank=True, null=True)
    event = models.CharField(max_length=128, blank=True, null=True)
    event_es = models.CharField(max_length=128, blank=True, null=True)
    event2 = models.CharField(max_length=128, blank=True, null=True)
    event2_es = models.CharField(max_length=128, blank=True, null=True)
    event3 = models.CharField(max_length=128, blank=True, null=True)
    event3_es = models.CharField(max_length=128, blank=True, null=True)
    play_guid = models.CharField(max_length=40, blank=True, null=True)
    home_team_runs = models.IntegerField(blank=True, null=True)
    away_team_runs = models.IntegerField(blank=True, null=True)

    score = models.CharField(max_length=3, blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

class Pitch(models.Model):

    # Maps reserved words used in external resources to their names in
    # this model
    reserved_fixes = {
        'id': 'external_id',
        'type': 'pitch_type',
    }

    atbat = models.ForeignKey(Atbat, on_delete=models.CASCADE)

    des = models.CharField(max_length=1028, blank=True, null=True)
    des_es = models.CharField(max_length=1028, blank=True, null=True)

    # This is the field that corresponds to "id" in the xml files. It has to be
    # renamed because "id" is reserved in django
    external_id = models.IntegerField(blank=True, null=True)

    # This is the field that corresponds to "type" in the xml files.
    # type is a reserved word in python
    pitch_type = models.CharField(max_length=3, blank=True, null=True)

    tfs = models.IntegerField(blank=True, null=True)
    tfs_zulu = models.DateTimeField(blank=True, null=True)
    x = models.DecimalField(max_digits=7, decimal_places=4, blank=True)
    y = models.DecimalField(max_digits=7, decimal_places=4, blank=True)
    event_num = models.IntegerField(blank=True, null=True)
    sv_id = models.CharField(max_length=40, blank=True, null=True)
    play_guid = models.CharField(max_length=40, blank=True, null=True)
    start_speed = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    end_speed = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    sz_top = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    sz_bot = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    pfx_x = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    pfx_z = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    px = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    pz = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    x0 = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    y0 = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    z0 = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    vx0 = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    vy0 = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    vz0 = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    ax = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    ay = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    az = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    break_y = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    break_angle = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    break_length = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    type_confidence = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    zone = models.IntegerField(blank=True, null=True)
    nasty = models.IntegerField(blank=True, null=True)
    spin_dir = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    spin_rate = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    mt = models.CharField(max_length=1000, blank=True, null=True)

    on_1b = models.IntegerField(blank=True, null=True)
    on_2b = models.IntegerField(blank=True, null=True)
    on_3b = models.IntegerField(blank=True, null=True)

    balls = models.IntegerField()
    strikes = models.IntegerField()

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
