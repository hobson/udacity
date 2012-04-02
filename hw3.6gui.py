#!/usr/bin/python2.6

from Tkinter import *
from hw3_6orig import *

from time import sleep

#Developped with Python 2.7.2
#
#   How to use it :
# 1)  Copy and save this file
# 2)  Copy your code in homework 3-6 and
#save it as hw3_6_ParticleFilter.py in the
#same directory
# 3)  Execute this file

#***************************************
class DispParticleFilter(Tk):

    '''frameLength is the delay between two frames, i.e. two steps of the filter'''
    def __init__(self, motions, N=500, frameLength = 0.5, displayRealRobot = True, displayGhost = False ):
        Tk.__init__(self)
        self.title( 'Diplay Particle Filter CS373-HW03.06')
        self.motions = motions        
        self.N = N
        self.bearing_noise = bearing_noise
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

        self.frameLength = frameLength
        self.displayRealRobot = displayRealRobot        
        self.displayGhost = displayGhost
        #init particle filter
        self.initFilter()
        # Drawing
        self.margin = 100                                    # margin
        self.zoom_factor = 2                                # zoom factor
        self.playing = False
        self.can = DisplayParticles ( self.margin, self.zoom_factor )
        self.can.configure(bg ='ivory', bd =2, relief=SUNKEN)
        self.can.pack(side =TOP, padx =5, pady =5)
        self.can.draw_all(self.p, self.robot, self.displayRealRobot, self.displayGhost)
        #Buttons
        self.controlFrame = Frame(self)
        self.buttonReset = Button(self.controlFrame, text ='Reset', command =self.resetFilter)
        self.buttonReset.pack(side =LEFT, padx =5, pady =5)
        self.buttonNext = Button(self.controlFrame, text ='Next step', command =self.nextStep)
        self.buttonNext.pack(side =LEFT, padx =5, pady =5)
        self.buttonPlay = Button(self.controlFrame, text ='Play', command =self.play)
        self.buttonPlay.pack(side =LEFT, padx =5, pady =5)
        self.buttonPause = Button(self.controlFrame, text ='Pause', command =self.pause)
        self.buttonPause.pack(side =LEFT, padx =5, pady =5)    
        self.buttonPause.configure(state=DISABLED)         
        #Label
        textLabel = 'Current state = ' + str(self.actualState+1) + '/' + str(len(motions))
        self.label = Label(self.controlFrame, text = textLabel )
        self.label.pack(side =LEFT, padx =5, pady =5)

        self.controlFrame.pack(side =BOTTOM,fill=X)
        self.createOptionsPanel()

    def createOptionsPanel(self):
        self.optionsFrame = Frame(self, {"bd":2} )
        # Number of Particles
        self.partNumVar = IntVar()
        self.partNumVar.set(self.N)
        self.partNumVar.trace("w", self.setParticleCount)
        textLab = 'Particle #: '
        self.partNumLabel = Label(self.optionsFrame, text = textLab)
        self.partNumLabel.pack(side=LEFT, padx=5, pady=5)
        self.partNumEntry = Entry(self.optionsFrame, textvariable=self.partNumVar, width=5)
        self.partNumEntry.pack(side=LEFT, padx=5, pady=5)

        # Bearing Noise
        self.bearingNoiseVar = StringVar()
        self.bearingNoiseVar.set(self.bearing_noise)
        self.bearingNoiseVar.trace("w", self.setBearingNoise)
        textLab = 'Bearing Noise: '
        self.bearingNoiseLabel = Label(self.optionsFrame, text = textLab)
        self.bearingNoiseLabel.pack(side=LEFT, padx=5, pady=5)
        self.bearingNoiseEntry = Entry(self.optionsFrame, textvariable=self.bearingNoiseVar, width=5)
        self.bearingNoiseEntry.pack(side=LEFT, padx=5, pady=5)

        # Steering Noise
        self.steeringNoiseVar = StringVar()
        self.steeringNoiseVar.set(self.steering_noise)
        self.steeringNoiseVar.trace("w", self.setSteeringNoise)
        textLab = 'Steering Noise: '
        self.steeringNoiseLabel = Label(self.optionsFrame, text = textLab)
        self.steeringNoiseLabel.pack(side=LEFT, padx=5, pady=5)
        self.steeringNoiseEntry = Entry(self.optionsFrame, textvariable=self.steeringNoiseVar, width=5)
        self.steeringNoiseEntry.pack(side=LEFT, padx=5, pady=5)

        # distance Noise
        self.distanceNoiseVar = StringVar()
        self.distanceNoiseVar.set(self.distance_noise)
        self.distanceNoiseVar.trace("w", self.setDistanceNoise)
        textLab = 'Distance Noise: '
        self.distanceNoiseLabel = Label(self.optionsFrame, text = textLab)
        self.distanceNoiseLabel.pack(side=LEFT, padx=5, pady=5)
        self.distanceNoiseEntry = Entry(self.optionsFrame, textvariable=self.distanceNoiseVar, width=5)
        self.distanceNoiseEntry.pack(side=LEFT, padx=5, pady=5)

        self.optionsFrame.pack(side =BOTTOM,fill=X)

    def setParticleCount(self, *args):
        self.N = int(self.partNumVar.get())

    def setBearingNoise(self, *args):
        bearing_noise_val = float(self.bearingNoiseVar.get())
        self.bearing_noise = 0.0001 if bearing_noise_val == 0 else bearing_noise_val
        self.bearingNoiseVar.set(self.bearing_noise)

    def setSteeringNoise(self, *args):
        self.steering_noise = float(self.steeringNoiseVar.get())

    def setDistanceNoise(self, *args):
        self.distance_noise = float(self.distanceNoiseVar.get())

    def resetFilter(self):
        self.pause()

        self.initFilter()
        #Replot all
        self.can.draw_all(self.p, self.robot, self.displayRealRobot, self.displayGhost)

    def initFilter (self):

        #New Robot's position
        self.robot = robot()
        self.robot.set_noise(bearing_noise, steering_noise, distance_noise)

        # Make particles            
        self.p = []                     # p : particles set
        for i in range(self.N):
            r = robot()
            r.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)
            self.p.append(r)
        # --------------
        self.actualState = 0

    def nextStep (self, event=None):
        self.actualState = self.actualState + 1
        if self.actualState < len(self.motions):
            #Label
            stateString = 'Actual state = ' + str(self.actualState+1) + '/' + str(len(motions))
            self.label.configure( text = stateString )
            # motion update (prediction)
            self.robot = self.robot.move(self.motions[self.actualState])
            p2 = []
            for i in range(self.N):
                p2.append(self.p[i].move(self.motions[self.actualState]))
            self.p = p2
            # measurement update
            w = []
            for i in range(self.N):
                w.append(self.p[i].measurement_prob( self.robot.sense() ))
            # resampling
            p3 = []
            index = int(random.random() * self.N)
            beta = 0.0
            mw = max(w)
            for i in range(self.N):
                beta += random.random() * 2.0 * mw
                while beta > w[index]:
                    beta -= w[index]
                    index = (index + 1) % self.N
                p3.append(self.p[index])
            self.p = p3
            #Replot all
            self.can.draw_all(self.p, self.robot, self.displayRealRobot, self.displayGhost)
            return True
        else:
            return False

    def play (self, event=None):
        self.playing = True
        self.buttonPause.configure(state=NORMAL)  
        self.buttonNext.configure(state=DISABLED) 
        self.buttonPlay.configure(state=DISABLED) 
        while self.playing:
            if self.nextStep() == False:
                self.pause(event)
                self.buttonPlay.configure(state=DISABLED)  
                self.buttonNext.configure(state=DISABLED)                 
                break
            self.update()
            sleep(self.frameLength)

    def pause (self, event=None):
        self.playing = False
        self.buttonPause.configure(state=DISABLED)  
        self.buttonNext.configure(state=NORMAL) 
        self.buttonPlay.configure(state=NORMAL)

class DisplayParticles(Canvas):

    def __init__(self, margin, zoom_factor ):
        Canvas.__init__(self)
        #self.p = p
        self.margin = margin
        self.zoom_factor = zoom_factor
        self.larg = (2*margin + world_size) * zoom_factor
        self.haut = self.larg
        self.configure(width=self.larg, height=self.haut )
        self.larg, self.haut = (2*margin + world_size) * zoom_factor, (2*margin + world_size) * zoom_factor
        # Landmarks
        self.landmarks_radius = 2
        self.landmarks_color = 'green'
        # Particles
        self.particle_radius = 1
        self.particle_color = 'red'
        # Robot
        self.robot_radius = 4
        self.robot_color = 'blue'
        self.ghost_color = None

    def draw_all(self, p, realRob, displayRealRobot, displayGhost):
        #print len(p)
        self.configure(bg ='ivory', bd =2, relief=SUNKEN)
        self.delete(ALL)
        self.p = p
        self.plot_particles()

        if displayGhost:
            ghost = get_position(self.p)
            self.plot_robot( ghost[0], ghost[1], ghost[2], self.robot_radius, self.ghost_color)
        self.plot_landmarks( landmarks, self.landmarks_radius, self.landmarks_color )

        if displayRealRobot:
            self.plot_robot( realRob.x, realRob.y, realRob.orientation, self.robot_radius, self.robot_color)

    def plot_landmarks(self, lms, radius, l_color ):
        for lm in lms:
            x0 = (self.margin + lm[1] - radius) * self.zoom_factor
            y0 = (self.margin + lm[0] - radius) * self.zoom_factor
            x1 = (self.margin + lm[1] + radius) * self.zoom_factor
            y1 = (self.margin + lm[0] + radius) * self.zoom_factor
            self.create_oval( x0, y0, x1, y1, fill = l_color )

    def plot_particles(self):
        for particle in self.p:
            self.draw_particle( particle, self.particle_radius, self.particle_color )

    def draw_particle(self, particle, radius, p_color):
        #x0 = (self.margin + particle.x - radius) * self.zoom_factor
        #y0 = (self.margin + particle.y - radius) * self.zoom_factor
        #x1 = (self.margin + particle.x + radius) * self.zoom_factor
        #y1 = (self.margin + particle.y + radius) * self.zoom_factor
        #self.create_oval( x0, y0, x1, y1, fill = p_color )
        x2 = (self.margin + particle.x) * self.zoom_factor
        y2 = (self.margin + particle.y) * self.zoom_factor
        x3 = (self.margin + particle.x + 2*radius*cos(particle.orientation)) * self.zoom_factor
        y3 = (self.margin + particle.y + 2*radius*sin(particle.orientation)) * self.zoom_factor
        self.create_line( x2, y2, x3, y3, fill = p_color, width =self.zoom_factor,
                          arrow=LAST, arrowshape=(2*self.zoom_factor,
                                                  3*self.zoom_factor,
                                                  1*self.zoom_factor) )

    def plot_robot(self, x,y, orientation, radius, r_color):
        x0 = (self.margin + x - radius) * self.zoom_factor
        y0 = (self.margin + y - radius) * self.zoom_factor
        x1 = (self.margin + x + radius) * self.zoom_factor
        y1 = (self.margin + y + radius) * self.zoom_factor
        self.create_oval( x0, y0, x1, y1, fill = r_color )
        x2 = (self.margin + x) * self.zoom_factor
        y2 = (self.margin + y) * self.zoom_factor
        x3 = (self.margin + x + 2*radius*cos(orientation)) * self.zoom_factor
        y3 = (self.margin + y + 2*radius*sin(orientation)) * self.zoom_factor
        self.create_line( x2, y2, x3, y3, fill = r_color, width =self.zoom_factor, arrow=LAST )

#**************************************************

if __name__ == "__main__":
    #motions  ( here copy of the dataset in hw3-6 )
    number_of_iterations = 20
    motions = [[2. * pi / 20, 12.] for row in range(number_of_iterations)]

    #Display window
    wind = DispParticleFilter ( motions, 500, 0.1, displayRealRobot = True, displayGhost = True )
    wind.mainloop()
