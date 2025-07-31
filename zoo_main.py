import random
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from abc import ABC, abstractmethod

# --- Classes ---

class Animal(ABC):
    def __init__(self, name):
        self.name = name
        self.species = 'Animal'
        self.hunger = 50
        self.mood = "calm"
        self.age = 0
        self.energy = 100
        self.favorite_food = None
        self.hated_food = None

    def care(self):
        if self.mood == 'irritated' or self.energy < 40:
            self.energy = min(100, self.energy + 20)
            self.hunger += 10
            self.mood = 'calm'
            return f'{self.name} feels better. Energy: {self.energy}, Mood: {self.mood}'
        else:
            return f'{self.name} does not need care right now.'

    def random_event(self, zoo):
        chance = random.random()

        if chance < 0.1:
            self.energy = max(0, self.energy - 30)
            self.mood = 'irritated'
            return f'{self.name} got sick...'
        elif chance < 0.15:
            opponents = [a for a in zoo.animals if a.species == self.species and a != self]
            if opponents:
                opponent = random.choice(opponents)
                self.energy = max(0, self.energy - 20)
                opponent.energy = max(0, opponent.energy - 20)
                self.mood = 'irritated'
                opponent.mood = 'irritated'
                return f'{self.name} fought with {opponent.name}!'
        elif chance < 0.18 and 500 <= self.age <= 900:
            baby_name = self.name + '_jr'
            baby = type(self)(baby_name)
            baby.age = 0
            baby.hunger = 30
            baby.energy = 60
            zoo.add_animal(baby)
            return f'{self.name} gave birth to a baby: {baby_name}'
        return None

    def update_mood(self):
        if self.hunger > 80:
            self.mood = 'irritated'
        elif self.hunger > 50:
            self.mood = 'calm'
        else:
            self.mood = 'happy'

    def eat(self, food):
        if food.food_type not in self.diet:
            return f'{self.name} refuses to eat {food.name}. It is not in their diet!'
        if food.food_type == self.hated_food:
            self.mood = 'irritated'
            return f'{self.name} hates {food.name} and refuses to eat it.'
        hunger_reduction = food.nutrition
        if food.food_type == self.favorite_food:
            hunger_reduction += 10
            self.mood = 'happy'
            extra = f'{self.name} loves {food.name}! Very happy!'
        else:
            extra = ''
        self.hunger = max(0, self.hunger - hunger_reduction)
        self.update_mood()
        return f'{self.name} ate. Hunger: {self.hunger}, Mood: {self.mood}. {extra}'

    @abstractmethod
    def make_sound(self):
        pass

    def info(self):
        return f'{self.species} named {self.name}'

    def status(self):
        return f'{self.name} ({self.species}) | Age: {self.age} | Hunger: {self.hunger} | Mood: {self.mood} | Energy: {self.energy}'

    def pass_day(self):
        self.age += 1
        self.hunger += 20
        self.update_mood()

    def play(self):
        if self.age >= 300:
            return f'{self.name} does not want to play – too old.'
        if self.energy < 30:
            return f'{self.name} is too tired to play.'
        self.energy -= 30
        self.hunger += 10
        self.mood = 'happy'
        return f'{self.name} played and became happier!'

    def sleep(self):
        energy_gain = 40 if self.age < 500 else 20
        self.energy = min(100, self.energy + energy_gain)
        self.hunger += 5 if self.age < 500 else 15
        return f'{self.name} slept. Energy: {self.energy}'


class Food:
    def __init__(self, name, food_type, nutrition):
        self.name = name
        self.food_type = food_type
        self.nutrition = nutrition


class Lion(Animal):
    def __init__(self, name):
        super().__init__(name)
        self.species = 'Lion'
        self.diet = ['meat']
        self.favorite_food = 'meat'
        self.hated_food = 'grass'

    def eat(self, food):
        if self.mood == 'irritated':
            return f'{self.name} is too angry to eat.'
        result = super().eat(food)
        return result + f' {self.name} growls happily after the meat.'

    def make_sound(self):
        return f'{self.name} roars!'


class Elephant(Animal):
    def __init__(self, name):
        super().__init__(name)
        self.species = 'Elephant'
        self.diet = ['grass', 'fruits']
        self.favorite_food = 'fruits'
        self.hated_food = 'meat'

    def eat(self, food):
        if self.mood == 'irritated':
            return f'{self.name} is too angry to eat.'
        result = super().eat(food)
        return result + f' {self.name} trumpets after eating.'

    def make_sound(self):
        return f'{self.name} trumpets!'


class Penguin(Animal):
    def __init__(self, name):
        super().__init__(name)
        self.species = 'Penguin'
        self.diet = ['fish', 'small fish']
        self.favorite_food = 'small fish'
        self.hated_food = 'grass'

    def eat(self, food):
        if self.mood == 'irritated':
            return f'{self.name} is too angry to eat.'
        result = super().eat(food)
        return result + f' {self.name} chirps happily.'

    def make_sound(self):
        return f'{self.name} squeaks loudly!'


class Zoo:
    def __init__(self):
        self.animals = []
        self.food_storage = {
            'meat': 3,
            'grass': 5,
            'fish': 4,
            'small fish': 2,
            'fruits': 2
        }
        self.balance = 1000
        self.food_prices = {
            'meat': 50,
            'grass': 10,
            'fish': 30,
            'small fish': 25,
            'fruits': 20
        }
        self.care_cost_per_animal = 120
        self.ticket_price = 100

    def buy_food(self, food_type, amount):
        cost = self.food_prices.get(food_type, 0) * amount
        if cost > self.balance:
            return f'Not enough money to buy {amount} units of {food_type}. Need {cost}, have {self.balance}.'
        self.balance -= cost
        self.food_storage[food_type] = self.food_storage.get(food_type, 0) + amount
        return f'Bought {amount} units of {food_type} for {cost} money. Balance: {self.balance}'

    def earn_from_visitors(self):
        happy_animals = sum(1 for a in self.animals if a.mood == 'happy')
        irritated_animals = sum(1 for a in self.animals if a.mood == 'irritated')
        visitors = len(self.animals) * 10
        visitors += happy_animals * 5
        visitors -= irritated_animals * 7
        visitors = max(0, visitors)
        income = visitors * self.ticket_price
        self.balance += income
        return f'{visitors} visitors came to the zoo. Earned {income} money. Balance: {self.balance}'

    def pay_care_costs(self):
        cost = len(self.animals) * self.care_cost_per_animal
        if cost > self.balance:
            return f'Not enough money to care for animals! Need {cost}, have {self.balance}.'
        else:
            self.balance -= cost
            return f'Paid {cost} for animal care. Balance: {self.balance}'

    def add_animal(self, animal):
        if isinstance(animal, Animal):
            self.animals.append(animal)
            return f'{animal.species} named {animal.name} added to the zoo.'
        else:
            return 'Error: can only add objects inherited from Animal.'

    def remove_animal(self, name):
        for animal in self.animals:
            if animal.name.lower() == name.lower():
                self.animals.remove(animal)
                return f'{animal.species} named {name} removed from the zoo.'
        return f'No animal named {name} found.'

    def show_all(self):
        if not self.animals:
            return 'No animals in the zoo.'
        return '\n'.join(animal.info() for animal in self.animals)

    def feed_all(self):
        messages = []
        food_by_species = {
            'Lion': ('meat', Food('Meat', 'meat', 30)),
            'Elephant': ('fruits', Food('Fruits', 'fruits', 25)),
            'Penguin': ('small fish', Food('Small Fish', 'small fish', 20))
        }
        for animal in self.animals:
            food_info = food_by_species.get(animal.species)
            if not food_info:
                messages.append(f'No suitable food for {animal.species}')
                continue
            food_type, food = food_info
            if self.food_storage.get(food_type, 0) > 0:
                msg = animal.eat(food)
                self.food_storage[food_type] -= 1
                messages.append(msg)
            else:
                messages.append(f'No {food_type} left to feed {animal.name}')
        return '\n'.join(messages)

    def daily_update(self):
        messages = []
        for animal in self.animals[:]:  # copy list because may add baby animals
            animal.pass_day()
            event = animal.random_event(self)
            if event:
                messages.append(event)
        care_message = self.pay_care_costs()
        messages.append(care_message)
        visitors_message = self.earn_from_visitors()
        messages.append(visitors_message)
        return '\n'.join(messages)

    def play_with_animal(self, name):
        for animal in self.animals:
            if animal.name.lower() == name.lower():
                return animal.play()
        return f'No animal named {name} found.'

    def put_to_sleep(self, name):
        for animal in self.animals:
            if animal.name.lower() == name.lower():
                return animal.sleep()
        return f'No animal named {name} found.'

# --- GUI ---

class ZooApp:
    def __init__(self, master):
        self.zoo = Zoo()

        master.title("Zoo Simulator")

        self.text_area = scrolledtext.ScrolledText(master, width=60, height=25)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.status_button = tk.Button(master, text="Show All Animals", command=self.show_animals)
        self.status_button.grid(row=1, column=0, pady=5)

        self.feed_button = tk.Button(master, text="Feed All Animals", command=self.feed_animals)
        self.feed_button.grid(row=1, column=1, pady=5)

        self.daily_button = tk.Button(master, text="Advance Day", command=self.advance_day)
        self.daily_button.grid(row=1, column=2, pady=5)

        self.add_button = tk.Button(master, text="Add Animal", command=self.add_animal)
        self.add_button.grid(row=2, column=0, pady=5)

        self.remove_button = tk.Button(master, text="Remove Animal", command=self.remove_animal)
        self.remove_button.grid(row=2, column=1, pady=5)

        self.play_button = tk.Button(master, text="Play with Animal", command=self.play_animal)
        self.play_button.grid(row=2, column=2, pady=5)

        self.sleep_button = tk.Button(master, text="Put Animal to Sleep", command=self.sleep_animal)
        self.sleep_button.grid(row=2, column=3, pady=5)

        self.buy_food_button = tk.Button(master, text="Buy Food", command=self.buy_food)
        self.buy_food_button.grid(row=3, column=0, pady=5)

        self.balance_label = tk.Label(master, text=f'Balance: {self.zoo.balance}')
        self.balance_label.grid(row=3, column=1, pady=5)

        self.food_storage_label = tk.Label(master, text=self.get_food_storage_text())
        self.food_storage_label.grid(row=3, column=2, columnspan=2, pady=5)

    def show_animals(self):
        self.text_area.delete('1.0', tk.END)
        if not self.zoo.animals:
            self.text_area.insert(tk.END, "No animals in the zoo.\n")
            return
        for animal in self.zoo.animals:
            self.text_area.insert(tk.END, animal.status() + "\n")

    def feed_animals(self):
        msg = self.zoo.feed_all()
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, msg + "\n")
        self.update_food_storage()
        self.update_balance()

    def advance_day(self):
        msg = self.zoo.daily_update()
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, msg + "\n")
        self.update_food_storage()
        self.update_balance()

    def add_animal(self):
        species = simpledialog.askstring("Add Animal", "Enter species (Lion, Elephant, Penguin):")
        if species is None:
            return
        name = simpledialog.askstring("Add Animal", "Enter animal name:")
        if name is None:
            return
        species = species.strip().lower()
        if species == 'lion':
            animal = Lion(name)
        elif species == 'elephant':
            animal = Elephant(name)
        elif species == 'penguin':
            animal = Penguin(name)
        else:
            messagebox.showerror("Error", "Unknown species.")
            return
        msg = self.zoo.add_animal(animal)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, msg + "\n")
        self.show_animals()

    def remove_animal(self):
        name = simpledialog.askstring("Remove Animal", "Enter animal name to remove:")
        if name is None:
            return
        msg = self.zoo.remove_animal(name)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, msg + "\n")
        self.show_animals()

    def play_animal(self):
        name = simpledialog.askstring("Play", "Enter animal name to play with:")
        if name is None:
            return
        msg = self.zoo.play_with_animal(name)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, msg + "\n")
        self.show_animals()

    def sleep_animal(self):
        name = simpledialog.askstring("Sleep", "Enter animal name to put to sleep:")
        if name is None:
            return
        msg = self.zoo.put_to_sleep(name)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, msg + "\n")
        self.show_animals()

    def buy_food(self):
        food_type = simpledialog.askstring("Buy Food", "Enter food type (meat, grass, fish, small fish, fruits):")
        if food_type is None:
            return
        try:
            amount = int(simpledialog.askstring("Buy Food", "Enter amount to buy:"))
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount.")
            return
        msg = self.zoo.buy_food(food_type.strip().lower(), amount)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, msg + "\n")
        self.update_food_storage()
        self.update_balance()

    def update_balance(self):
        self.balance_label.config(text=f'Balance: {self.zoo.balance}')

    def get_food_storage_text(self):
        return "Food Storage: " + ', '.join(f"{k}: {v}" for k, v in self.zoo.food_storage.items())

    def update_food_storage(self):
        self.food_storage_label.config(text=self.get_food_storage_text())


if __name__ == '__main__':
    root = tk.Tk()
    app = ZooApp(root)
    root.mainloop()
