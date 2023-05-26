# modul 
import pygame # untuk pembuatan game
import random # untuk memberikan angka acak kemuculan tikus
from pygame import *

# class utama untuk mengelola game
class GameManager:
    def __init__(self):
        # inisialisasi konstanta
        self.SCREEN_WIDTH = 800 #ukuran layar
        self.SCREEN_HEIGHT = 600 #ukuran layar
        self.FPS = 60 #jumlah frame tiap detiknya
        self.MOLE_WIDTH = 90 #ukuran tikus
        self.MOLE_HEIGHT = 81 #ukuran tikus
        self.FONT_SIZE = 31 #ukuran font
        self.FONT_TOP_MARGIN = 26 #ukuran margin atas 
        self.LEVEL_SCORE_GAP = 5 #jarak poin tiap level
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "Whac A Mole"
        # Inisialisasi skor player, miss, dan level
        self.__score = 0 # score atau poin 
        self.__misses = 0 # miss atau ketidaktepatan pukulan
        self.__level = 1 # level
        # Sound effect
        self.soundEffect = SoundEffect()


        # Inisialisasi display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("images/bg.png")

        # Font untuk tampilan teks pada game
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', self.FONT_SIZE)
        
        # Memuat gambar mole
        # 6 bagian yang berbeda
        sprite_sheet = pygame.image.load("images/mole.png")
        # membuat list untuk gambar mole
        self.mole = []
        # Memotong bagian tertentu dari sprite sheet
        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
        
        # membuat list untuk posisi lubang di background
        self.hole_positions = []
        # meletakkan lubang di layar seuai posisi 
        self.hole_positions.append((381, 295))
        self.hole_positions.append((119, 366))
        self.hole_positions.append((179, 169))
        self.hole_positions.append((404, 479))
        self.hole_positions.append((636, 366))
        self.hole_positions.append((658, 232))
        self.hole_positions.append((464, 119))
        self.hole_positions.append((95, 43))
        self.hole_positions.append((603, 11))


    # menghitung level pemain berdasarkan skornya saat ini dan LEVEL_SCORE_GAP
    def get_player_level(self):
        # inisialisasi dengan nilai level baru
        newLevel = 1 + int(self.__score / self.LEVEL_SCORE_GAP)
        # Jika level baru berbeda dengan level sebelumnya
        if newLevel != self.__level:
            # memainkan sound jika player naik level
            self.soundEffect.playLevelUp()
        # mengembalikan nilai level baru yang dihitung berdasarkan skor pemain
        return 1 + int(self.__score / self.LEVEL_SCORE_GAP)

    # mendapatkan durasi baru antara waktu mole muncul dan turun lubang
    def get_interval_by_level(self, initial_interval):
        # semakin tinggi level, semakin pendek durasi barunya
        new_interval = initial_interval - self.__level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    # memeriksa apakah klik mouse mengenai mole atau tidak
    def is_mole_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        # apakah posisi klik mouse berada di dalam batas area posisi lubang & mole
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.MOLE_HEIGHT):
            return True
        else:
            return False

        
    # mengupdate status game, rekalkulasi player __score, misses, level
    def update(self):
        # Update jumlah skor player
        current_score_string = "SCORE: " + str(self.__score) # inisialisasi string "SCORE: " + nilai skor 
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255)) # render menjadi permukaan teks
        score_text_pos = score_text.get_rect() # membuat persegi panjang yang mengelilingi teks skor untuk mengatur posisi teks
        score_text_pos.centerx = self.background.get_rect().centerx # mengatur posisi horisontal teks
        score_text_pos.centery = self.FONT_TOP_MARGIN # mengatur posisi vertikal teks pada layar
        self.screen.blit(score_text, score_text_pos) # menggambar teks skor ke permukaan layar
        # Update jumlah miss player
        current_misses_string = "MISSES: " + str(self.__misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)
        # Update status level player
        current_level_string = "LEVEL: " + str(self.__level)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 5 * 1
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)

    # dipanggil saat game berakhir
    def game_over(self):
        # menampilkan pesan game over 
        game_over_text = self.font_obj.render("GAME OVER", True, (255, 255, 255))
        score_text = self.font_obj.render("Final Score: " + str(self.__score), True, (255, 255, 255))
        game_over_text_pos = game_over_text.get_rect()
        score_text_pos = score_text.get_rect()
        game_over_text_pos.centerx = self.background.get_rect().centerx
        game_over_text_pos.centery = self.background.get_rect().centery
        score_text_pos.centerx = self.background.get_rect().centerx
        score_text_pos.centery = self.SCREEN_HEIGHT / 2-50
        self.screen.blit(game_over_text, game_over_text_pos)
        self.screen.blit(score_text, score_text_pos)

        # untuk memperbarui tampilan layar
        pygame.display.update()
        
        # untuk memberi jeda program selama 5 detik 
        pygame.time.wait(5000)

        # kembali ke home screen
        screen.home_screen()


    # Start main loop
    # Berisi beberapa logika untuk menangani event, animasi, dll..
    def start(self):
        self.__score = 0 # score atau poin 
        self.__misses = 0 # miss atau ketidaktepatan pukulan
        self.__level = 1 # level

        # variabel ini digunakan dalam logika permainan dan animasi
        cycle_time = 0
        num = -1
        loop = True
        is_down = False
        interval = 0.1
        initial_interval = 1
        frame_num = 0
        left = 0
        # untuk mengontrol waktu dalam permainan
        clock = pygame.time.Clock()

        # loop sebanyak elemen dalam self.mole
        for i in range(len(self.mole)):
            # menyusun ulang gambar-gambar "mole" 
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()


        # Memulai loop utama permainan
        # Berisi beberapa logika untuk menangani event, animasi, dll..
        while loop:
            # untuk mengambil semua event Pygame yang terjadi
            for event in pygame.event.get():
                # jika user menutup jendela permainan maka loop berhenti
                if event.type == pygame.QUIT:
                    loop = False
                # jika tombol kiri mouse diklik, maka dilakukan beberapa aksi
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                    self.soundEffect.playFire() # memainkan backsound fire
                    # jika mouse klik mengenai posisi mole
                    if self.is_mole_hit(mouse.get_pos(), self.hole_positions[frame_num]) and num > 0 and left == 0:
                        
                        # untuk mengatur animasi "mole"
                        num = 3
                        left = 14
                        is_down = False
                        interval = 0

                        self.__score += 1  # menambah score player jika mengenai mole
                        self.__level = self.get_player_level()  # kalkulasi player level
                        self.soundEffect.stopPop() # play sound effect stop popping 
                        self.soundEffect.playHurt() # play sound effect  hurt sound
                        self.update()
                    else:
                        # jika mouse klik tidak mengenai mole
                        self.__misses += 1 # menambah poin misses
                        self.update()

            # mengatur latar belakang dan reset variabel terkait animasi "mole"
            if num > 5:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = -1
                left = 0

            if num == -1:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = 0
                is_down = False
                interval = 0.5
                frame_num = random.randint(0, 8)

            
            mil = clock.tick(self.FPS) # batasan kecepatan frame per detik (FPS)
            sec = mil / 1000.0 
            cycle_time += sec # total waktu yang telah berlalu sejak pemanggilan fungsi clock.tick() terakhir
            
            # Jika waktu yang telah berlalu melebihi interval yang ditentukan
            if cycle_time > interval:

                # animasi mole diubah
                pic = self.mole[num]
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1])) #
                self.update()
                if is_down is False:
                    num += 1
                else:
                    num -= 1
                if num == 4:
                    interval = 0.3
                elif num == 3:
                    num -= 1
                    is_down = True
                    self.soundEffect.playPop()
                    interval = self.get_interval_by_level(initial_interval)  
                else:
                    interval = 0.1
                cycle_time = 0
            
            pygame.display.flip() # tampilan layar diperbarui 

            # jika misses mencapai 5 maka game dinyatakan berakhir
            if self.__misses >= 5:
                pygame.mixer.music.stop() # background music berhenti
                self.soundEffect.playGameOver() # music "game over" dimainkan
                self.game_over() # pemanggilan fungsi game over

# class untuk mengelola tampilan layar awal
class HomeScreen(GameManager):
    def __init__(self):
        # memanggil metode __init__ dari superclass GameManager
        super().__init__()
        self.is_running = True

        # Memuat gambar seperti background, tombol start, quit, judul, dan mole
        # Mengambil objek persegi panjang (Rect) yang mengelilingi gambar dan mengatur posisi dilayar
        self.home_bg = pygame.image.load("images/home_bg.png") 
        self.start_button = pygame.image.load("images/start_button.png")
        self.start_button_rect = self.start_button.get_rect(center=(self.SCREEN_WIDTH / 2-130, self.SCREEN_HEIGHT / 2+70))
        self.quit_button = pygame.image.load("images/quit_button.png")
        self.quit_button_rect = self.quit_button.get_rect(center=(self.SCREEN_WIDTH / 2-140, self.SCREEN_HEIGHT / 2+160))
        self.choose_title = pygame.image.load("images/choose_title.png") # Lo
        self.choose_title_rect = self.choose_title.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 180))
        self.original = pygame.image.load("images/original_mole.png")
        self.original_rect = self.original.get_rect(center=(self.SCREEN_WIDTH / 2-230, self.SCREEN_HEIGHT/2+20))
        self.redmole = pygame.image.load("images/red_mole.png")
        self.redmole_rect = self.redmole.get_rect(center=(self.SCREEN_WIDTH / 2-5, self.SCREEN_HEIGHT/2+20))
        self.bluemole = pygame.image.load("images/blue_mole.png")
        self.bluemole_rect = self.bluemole.get_rect(center=(self.SCREEN_WIDTH / 2+ 225, self.SCREEN_HEIGHT/2+20))

    # fungsi untuk memilih diantara 3 jenis mole
    def choose_mole(self):
        # memuat gambar latar belakang
        self.home_bg = pygame.image.load("images/home_bg2.png")

        while self.is_running:
            # untuk mengambil setiap event yang terjadi
            for event in pygame.event.get():
                # jika user menutup jendela permainan maka loop berhenti
                if event.type == QUIT:
                    self.is_running = False
                    pygame.quit()
                # jika tombol kiri mouse diklik, maka dilakukan beberapa aksi
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                    mouse_pos = pygame.mouse.get_pos() # mendapatkan posisi mouse saat diklik
                    
                    # terdapat 3 pilihan warna mole 
                    # jika mole 1 dipilih maka akan dimuat gambar sprite sheet mole cokelat (original)
                    if self.original_rect.collidepoint(mouse_pos):
                        self.soundEffect.playFire()
                        sprite_sheet = pygame.image.load("images/mole.png")
                        # membuat list untuk gambar mole
                        self.mole = []
                        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
                        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
                        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
                        # Start game
                        self.start()

                    # jika mole 2 dipilih maka akan dimuat gambar sprite sheet mole biru
                    elif self.bluemole_rect.collidepoint(mouse_pos):
                        self.soundEffect.playFire()
                        sprite_sheet = pygame.image.load("images/mole2.png")
                        # membuat list untuk gambar mole
                        self.mole = []
                        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
                        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
                        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
                         # Start game
                        self.start()

                    # jika mole 3 dipilih maka akan dimuat gambar sprite sheet mole merah
                    elif self.redmole_rect.collidepoint(mouse_pos):
                        self.soundEffect.playFire()
                        sprite_sheet = pygame.image.load("images/mole3.png")
                        # membuat list untuk gambar mole
                        self.mole = []
                        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
                        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
                        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
                        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
                        # Quit game
                        self.start()
            # memuat gambar ke dalam layar
            self.screen.blit(self.home_bg, (0, 0))
            self.screen.blit(self.choose_title, self.choose_title_rect)
            self.screen.blit(self.original, self.original_rect)
            self.screen.blit(self.redmole, self.redmole_rect)
            self.screen.blit(self.bluemole, self.bluemole_rect)
            pygame.display.update() # memperbarui tampilan layar sesuai perubahan

    # untuk menampilkan layar awal sebelum memulai permainan
    def home_screen(self):
        self.home_bg = pygame.image.load("images/home_bg.png") # memuat gambar latar belakang
        pygame.mixer.music.play(-1) # memainkan musik latar belakang
        while self.is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_running = False
                    pygame.quit()
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                    mouse_pos = pygame.mouse.get_pos() # mengambil posisi mouse saat tombol diklik
                    # jika posisi mouse berada di dalam kotak start maka memanggil fungsi choose_mole
                    if self.start_button_rect.collidepoint(mouse_pos):
                        self.soundEffect.playFire()
                        self.choose_mole()
                    # jika posisi mouse berada di dalam kotak quit maka pygame berhenti
                    elif self.quit_button_rect.collidepoint(mouse_pos):
                        self.soundEffect.playFire()
                        self.is_running = False
                        pygame.quit()
            # memperbarui tampilan layar
            self.screen.blit(self.home_bg, (0, 0))
            pygame.display.update()


class SoundEffect:
    def __init__(self):
        # memuat sound effect
        self.mainTrack = pygame.mixer.music.load("sounds/themesong.wav")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        self.overSound = pygame.mixer.Sound("sounds/gameover.wav")
        
        # mengatur volume sound effect
        pygame.mixer.music.set_volume(0.1)
        self.fireSound.set_volume(0.2)
        self.popSound.set_volume(0.2)
        self.hurtSound.set_volume(0.2)
        self.levelSound.set_volume(0.2)
        self.overSound.set_volume(0.5)
        
        # memainkan background music
        pygame.mixer.music.play(-1)
    
    # fungsi untuk memainkan sound effect
    def playFire(self):
        self.fireSound.play()           
    def stopFire(self):
        self.fireSound.stop()
    def playPop(self):
        self.popSound.play()
    def stopPop(self):
        self.popSound.stop()
    def playHurt(self):
        self.hurtSound.play()
    def stopHurt(self):
        self.hurtSound.stop()
    def playLevelUp(self):
        self.levelSound.play()
    def stopLevelUp(self):
        self.levelSound.stop()
    def playGameOver(self):
        self.overSound.play()

# mengatur sound
# frequency(frekuensi standar 22050, size(ukuran bit data suara),
# channels(stereo), buffer(menyimpan audio sebelum diputar)
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# inisialisasi game 
pygame.init()
# menjalankan fungsi homescreen dan gamemanager.start
screen = HomeScreen()
screen.home_screen()
game = GameManager()
game.start()
# Exit game ketika main loop selesai
pygame.quit()