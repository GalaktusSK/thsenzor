#
import machine


# set the microcontroller's frequency
print(f'Current frequency is {machine.freq() // 1000000}MHz')
