from code_jam_site.bug_game.mapgen import generate_map
import random

from code_jam_site.bug_game.pathfind import pathfind

def initialize_game(player_ids):
    MAP_HORIZONTAL = 5
    MAP_VERTICAL = 5

    ROOM_HORIZONTAL = 80
    ROOM_VERTICAL = 80
    DOOR_CHAR = 3
    WALL_CHAR = 2
    ROCK_CHAR = 1
    NONE_CHAR = 0

    DOOR_FRAMES = [38, 39, 40, 41]
    enemy_count=200
    map=generate_map()
    playerlocs={}
    enemylocs={}
    for player in player_ids:
        spawnlocx=random.randint(16,1248)
        spanwlocy=random.randint(16,1248)
        while ((((map[0])[0])[spawnlocx//16])[spanwlocy//16])!=0:
            spawnlocx=random.randint(16,1248)
            spanwlocy=random.randint(16,1248)
        location=[0,0,spawnlocx,spanwlocy]
        playerlocs[player]=location
    for enemy_id in range(1,enemy_count):
        spawnlocx=random.randint(16,1248)
        spanwlocy=random.randint(16,1248)
        roomx=random.randint(0, 5)
        roomy=random.randint(0, 5)
        while ((((map[roomx])[roomy])[spawnlocx//16])[spanwlocy//16])!=0:
            spawnlocx=random.randint(16,1248)
            spanwlocy=random.randint(16,1248)  
            roomx=random.randint(0, 5)
            roomy=random.randint(0, 5)
        location=[roomx, roomy, spawnlocx,spanwlocy]
        enemylocs[str(enemy_id)]=location    

def player_input_handler(id, input, playerlocs,enemylocs map):
    playerloc=playerlocs[id]
    ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2]//16)])[((playerloc[3])//16)])
    if input=='up':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2]//16)])[((playerloc[3])//16)-1])!=0:
            return (playerlocs)
        elif playerloc[3]<16:
            newplayerloc=((((map[playerloc[0]])[(playerloc[1]-1)])[(playerloc[2])])[(playerloc[3]+1248)])
        else:
            newplayerloc=((((map[playerloc[0]])[(playerloc[1]-1)])[(playerloc[2])])[(playerloc[3]-16)])            
    elif input=='down':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2]//16)])[((playerloc[3])//16)+1])!=0:
            return (playerlocs)
        elif playerloc[3]>1248:
            newplayerloc=((((map[playerloc[0]])[(playerloc[1]+1)])[(playerloc[2])])[(playerloc[3]-1248)])
        else:
            newplayerloc=((((map[playerloc[0]])[(playerloc[1]+1)])[(playerloc[2])])[(playerloc[3]+16)])         
    elif input=='left':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2]//16)-1])[((playerloc[3])//16)])!=0:
            return (playerlocs)
        elif playerloc[2]<16:
            newplayerloc=((((map[(playerloc[0]-1)])[(playerloc[1])])[(playerloc[2]+1248)])[(playerloc[3])])
        else:
            newplayerloc=((((map[(playerloc[0]-1)])[(playerloc[1])])[(playerloc[2]-16)])[(playerloc[3])])
    elif input=='right':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2]//16)+1])[((playerloc[3])//16)-1])!=0:
            return (playerlocs)
        elif playerloc[2]>1248:
            newplayerloc=((((map[(playerloc[0]+1)])[(playerloc[1]-1)])[(playerloc[2]-1248)])[(playerloc[3])]) 
        else:   
            newplayerloc=((((map[(playerloc[0]+1)])[(playerloc[1]-1)])[(playerloc[2]-1248)])[(playerloc[3])]) 
    elif input=='attack':
        for key in enemylocs.keys():
            if (enemylocs[key])[0]==playerloc[0] and (enemylocs[key])[1]==playerloc[1] and (enemylocs[key])[2] in range((playerloc[2]-20, (playerloc[2]+20))) and (enemylocs[key])[2] in range((playerloc[3]-24, (playerloc[3]+24))):
                enemylocs=enemylocs.pop(key)
    for rekey in enemylocs.keys():
        if (enemylocs[key])[0]==playerloc[0] and (enemylocs[key])[1]==playerloc[1] and (enemylocs[key])[2] in range((playerloc[2]-20, (playerloc[2]+20))) and (enemylocs[key])[2] in range((playerloc[3]-8, (playerloc[3]+8))):
            return ([id,'death'])

def enemy_actions(playerlocs, enemylocs, enemy, map):
    for player in playerlocs.keys():
        if (playerlocs[player])[0]==(enemylocs[enemy])[0] and (playerlocs[player])[1]==(enemylocs[enemy])[1]:
            room=(map[(enemylocs[enemy])[0]])[(enemylocs[enemy])[1]]
            enemypos=((enemylocs[enemy])[2], (enemylocs[enemy])[3])
            playerpos=((playerlocs[player])[2], (playerlocs[player])[3])
            path=pathfind(room, enemypos, playerpos)
            newenemypos=path[1]
            (enemylocs[enemy])[2]=newenemypos[0]
            (enemylocs[enemy])[3]=newenemypos[1]

            

