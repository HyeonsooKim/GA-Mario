# 02. create_env
# 게임 환경 생성
import retro

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()     #게임을 껐다키는 것
# env.get_screen()    #화면정보를 가져올 것
# env.get_ram()   #RAM에 모든 데이터를 다 올려줌. RAM속에 데이터를 추출하면 게임정보에 대한 모든 정보를 불러올 수 있음

print(env)

screen = env.get_screen()

print(screen.shape)
print(screen)
