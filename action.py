
import pygame

import colors
import flower
import manager
from terrain import Terrain
import unit
import rabbit

class Action( unit.Unit ):

    def __init__( self, terrain, executor ):
        unit.Unit.__init__( self, terrain )

        self.active_listeners = {
            pygame.K_s:         self.action_seed,
            pygame.K_t:         self.action_thorns,
            pygame.K_p:         self.action_poison,
            pygame.K_BACKSPACE: self.action_cancel
        }

        self.executor = executor

        manager.restore_default()
        manager.update_current( unit.Unit.active().active_listeners )

    def action_seed( self, event ):
        #if self.executor.growth < 2:
            #return False
        if self.terrain.contains_unit(unit_type = flower.Flower):
            return False
        elif self.terrain.contains_unit(unit_type = flower.Obstacle):
            return False
        #elif self.terrain.contains_unit(unit_type = rabbit.Rabbit):
            #self.growth += 2
        else:
            #self.executor.growth -= 2
            flower.Flower( self.terrain )
            self.delete( None )
            return True

    def action_thorns( self, event ):
        #if self.executor.growth < 3:
            #return False
        if self.terrain.contains_unit(unit_type = flower.Flower):
            return False
        elif self.terrain.contains_unit(unit_type = flower.Obstacle):
            return False
        else:
            #self.executor.growth -= 3
            unit = flower.Obstacle( self.terrain )
            #unit.set_counter(3)
            self.delete( None )
            return True

    def action_poison( self, event ):
        return False
        #if self.executor.growth < 3:
            #return False
        if self.terrain.contains_unit(unit_type = flower.Obstacle):
            return False
        elif self.terrain.contains_unit(unit_type = flower.Flower):
            self.executor.growth -= 3
            self.set_counter(5)
            self.set_hit(2)
        elif self.terrain.contains_unit(unit_type = rabbit.Rabbit):
            self.executor.growth -= 3
            self.set_counter(5)
            self.set_hit(2)
        else:
            self.executor.growth -= 3
            unit = flower.Obstacle( self.terrain )
            unit.set_counter(5)
            self.terrain.multiplier = 0

            self.delete( None )
            return True

    def action_cancel( self, event ):
        self.delete( None )

        manager.restore_default()
        manager.update_current( unit.Unit.active().active_listeners )

        return False

    def draw( self, screen ):
        if self is unit.Unit.active():
            self.terrain.draw_border(screen, colors.BLUE)
            self.executor.terrain.draw_border(screen, colors.RED)

