#! /usr/bin/env python -3

import json
import os
import re
import sys
try:
  import main as ladxr
except ModuleNotFoundError:
  sys.path.insert(1, 'LADXR')
  import main as ladxr

import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.filedialog import askopenfilename

# Change this if you want a wider window -- don't set to 1 or you probably
# won't be able to see the "Generate" button
UI_COLUMNS = 3

# TODO: UI cleanup (for rom input especially)
# TODO: self.dump_cmd_button = tk.Button(self, text='Dump command line', command=self.dump_cmd)
# TODO: shareable settings codes
# TODO: keysanity as global/player option in multiworld
# TODO: When creating new frames, settings should be populated from the common settings

class LadxrUi(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()

    self.notebook = ttk.Notebook(self)
    self.frames = [tk.Frame(self.notebook)]
    self.notebook.add(self.frames[0], text='Common')
    self.multi = 1

    uifont = font.Font(family='Segoe UI', size=10)
    self.option_add('*Font', uifont)

    self.global_opts = [
      { 'text': 'Seed', 'arg': 'seed', 'type': 'string', 'default': '' },
      { 'text': 'Multiworld', 'arg': 'multiworld', 'type': 'multi', 'default': 1 },
      { 'text': 'Forward Factor', 'arg': 'forwardfactor', 'type': 'ff', 'default': 0.5 },
      { 'text': 'Race Mode', 'arg': 'race', 'type': 'boolean', 'default': False },
      { 'text': 'Spoiler Format', 'arg': 'spoilerformat', 'type': 'choice', 'choices': [
        { 'text': 'None', 'value': 'none' },
        { 'text': 'Console', 'value': 'console' },
        { 'text': 'Text', 'value': 'text' },
        { 'text': 'JSON', 'value': 'json' }
      ], 'default': 'none' }
    ]
    self.player_opts = [
      # Main
      { 'text': 'Logic', 'arg': 'logic', 'type': 'choice', 'choices': [
        { 'text': 'Casual', 'value': 'casual' },
        { 'text': 'Normal', 'value': 'normal' },
        { 'text': 'Hard', 'value': 'hard' },
        { 'text': 'Glitched', 'value': 'glitched' },
        { 'text': 'Hell', 'value': 'hell' }
      ], 'default': 'normal' },
      { 'text': 'Accessibility', 'arg': 'accessibility', 'type': 'choice', 'choices': [
        { 'text': '100% Locations', 'value': 'all' },
        { 'text': 'Beatable', 'value': 'goal' }
      ], 'default': 'all' },
      # Items
      { 'text': 'Randomize Heart Pieces', 'arg': 'heartpiece', 'type': 'boolean', 'default': True },
      { 'text': 'Randomize Seashells', 'arg': 'seashells', 'type': 'boolean', 'default': True },
      { 'text': 'Randomize Heart Containers', 'arg': 'heartcontainers', 'type': 'boolean', 'default': True },
      { 'text': 'Randomize Instruments', 'arg': 'instruments', 'type': 'boolean', 'default': False },
      { 'text': 'Randomize Witch', 'arg': 'witch', 'type': 'boolean', 'default': True },
      { 'text': 'Boomerang Mode', 'arg': 'boomerang', 'type': 'choice', 'choices': [
        { 'text': 'Normal (require lens)', 'value': 'default' },
        { 'text': 'Trade', 'value': 'trade' },
        { 'text': 'Gift', 'value': 'gift' }
      ], 'default': 'gift' },
      # Gameplay
      { 'text': 'Dungeon Items', 'arg': 'dungeon-items', 'type': 'choice', 'choices': [
        { 'text': 'Standard', 'value': 'standard' },
        { 'text': 'Map/Compass/Beak', 'value': 'localkeys' },
        { 'text': 'MCB + Small Key', 'value': 'localnightmarekey' },
        { 'text': 'Keysanity', 'value': 'keysanity' }
      ], 'default': 'standard' },
      { 'text': 'Random Start Location', 'arg': 'randomstartlocation', 'type': 'boolean', 'default': False },
      { 'text': 'Dungeon Shuffle', 'arg': 'dungeonshuffle', 'type': 'boolean', 'default': False },
      { 'text': 'Entrance Randomizer', 'arg': 'entranceshuffle', 'type': 'choice', 'choices': [
        { 'text': 'Default', 'value': 'none' },
        { 'text': 'Simple', 'value': 'simple' },
        { 'text': 'Advanced', 'value': 'advanced' },
        { 'text': 'Expert', 'value': 'expert' },
        { 'text': 'Insanity', 'value': 'insanity' }
      ], 'default': 'none' },
      { 'text': 'Boss Shuffle', 'arg': 'boss', 'type': 'choice', 'choices': [
        { 'text': 'Normal', 'value': 'default' },
        { 'text': 'Shuffle', 'value': 'shuffle' },
        { 'text': 'Randomize', 'value': 'random' }
      ], 'default': 'default' },
      { 'text': 'Miniboss Shuffle', 'arg': 'miniboss', 'type': 'choice', 'choices': [
        { 'text': 'Normal', 'value': 'default' },
        { 'text': 'Shuffle', 'value': 'shuffle' },
        { 'text': 'Randomize', 'value': 'random' }
      ], 'default': 'default' },
      { 'text': 'Goal', 'arg': 'goal', 'type': 'choice', 'choices': [
        { 'text': '8', 'value': '8' },
        { 'text': '7', 'value': '7' },
        { 'text': '6', 'value': '6' },
        { 'text': '5', 'value': '5' },
        { 'text': '4', 'value': '4' },
        { 'text': '3', 'value': '3' },
        { 'text': '2', 'value': '2' },
        { 'text': '1', 'value': '1' },
        { 'text': '0', 'value': '0' },
        { 'text': 'Egg Open', 'value': '-1' },
        { 'text': 'Random', 'value': 'random' },
        { 'text': 'Random (S)', 'value': 'open-4' },
        { 'text': 'Random (L)', 'value': '5-8' },
        { 'text': 'Raft', 'value': 'raft' },
        { 'text': 'Seashells (20)', 'value': 'seashells' },
        { 'text': 'Bingo (Line)', 'value': 'bingo' },
        { 'text': 'BINGO (Card)', 'value': 'bingo-full' },
      ], 'default': '8' },
      { 'text': 'Item Pool', 'arg': 'pool', 'type': 'choice', 'choices': [
        { 'text': 'Normal', 'value': 'normal' },
        { 'text': 'Casual', 'value': 'casual' },
        { 'text': 'Path of Pain', 'value': 'pain' },
        { 'text': 'More Keys', 'value': 'keyup' }
      ], 'default': 'normal' },
      { 'text': 'Health Mode', 'arg': 'hpmode', 'type': 'choice', 'choices': [
        { 'text': 'Normal', 'value': 'default' },
        { 'text': 'Inverted', 'value': 'inverted' },
        { 'text': 'Start with 1 heart', 'value': '1' },
        { 'text': 'Low Max', 'value': 'low' }
      ], 'default': 'default' },
      { 'text': 'Oracles Mode', 'arg': 'hard-mode', 'type': 'boolean', 'default': False },
      { 'text': 'Stealing', 'arg': 'steal', 'type': 'choice', 'choices': [
        { 'text': 'Always', 'value': 'always' },
        { 'text': 'Never', 'value': 'never' },
        { 'text': 'Normal', 'value': 'default' }
      ], 'default': 'always' },
      # Special
      { 'text': 'Bow Wow Mode', 'arg': 'bowwow', 'type': 'choice', 'choices': [
        { 'text': 'Disabled', 'value': 'normal' },
        { 'text': 'Enabled', 'value': 'always' },
        { 'text': 'Swordless', 'value': 'swordless' }
      ], 'default': 'normal' },
      { 'text': 'Overworld', 'arg': 'overworld', 'type': 'choice', 'choices': [
        { 'text': 'Normal', 'value': 'normal' },
        { 'text': 'Dungeon Dive', 'value': 'dungeondive' }
      ], 'default': 'normal' },
      { 'text': 'Owl Statue Items', 'arg': 'owlstatues', 'type': 'choice', 'choices': [
        { 'text': 'Never', 'value': 'none' },
        { 'text': 'Dungeons', 'value': 'dungeon' },
        { 'text': 'Overworld', 'value': 'overworld' },
        { 'text': 'All', 'value': 'both' }
      ], 'default': 'none' },
      # User
      { 'text': 'Quickswap with SELECT', 'arg': 'quickswap', 'type': 'choice', 'choices': [
        { 'text': 'Disabled', 'value': 'none' },
        { 'text': 'Swap A', 'value': 'a' },
        { 'text': 'Swap B', 'value': 'b' }
      ], 'default': 'none' },
      { 'text': 'Text Speed', 'arg': 'textmode', 'type': 'choice', 'choices': [
        { 'text': 'Fast', 'value': 'fast' },
        { 'text': 'Normal', 'value': 'default' },
        { 'text': 'No Text', 'value': 'none' }
      ], 'default': 'fast' },
      { 'text': 'Low HP Beeps', 'arg': 'lowhpbeep', 'type': 'choice', 'choices': [
        { 'text': 'Slow', 'value': 'slow' },
        { 'text': 'Normal', 'value': 'default' },
        { 'text': 'Disabled', 'value': 'none' }
      ], 'default': 'slow' },
      { 'text': 'Remove Flashing Lights', 'arg': 'remove-flashing-lights', 'type': 'boolean', 'default': True },
      # This default differs from web because speedbois will want Flock clips
      { 'text': 'Nag Messages', 'arg': 'nag-messages', 'type': 'boolean', 'default': True },
      { 'text': 'Sprites', 'arg': 'gfxmod', 'type': 'gfx', 'choices': [{ 'text': 'Default', 'value': 'default' }], 'default': 'default' },
      { 'text': 'Tunic', 'arg': 'linkspalette', 'type': 'choice', 'choices': [
        { 'text': 'Normal', 'value': '' },
        { 'text': 'Green', 'value': '0' },
        { 'text': 'Yellow', 'value': '1' },
        { 'text': 'Red', 'value': '2' },
        { 'text': 'Blue', 'value': '3' },
      ], 'default': '' },
      { 'text': 'Music', 'arg': 'music', 'type': 'choice', 'choices': [
        { 'text': 'Default', 'value': 'default' },
        { 'text': 'Random', 'value': 'random' },
        { 'text': 'Disabled', 'value': 'off' }
      ], 'default': 'default' }
    ]

    gfxopt = [o for o in self.player_opts if o['arg'] == 'gfxmod'][0]
    with open(os.path.join('Z4Randomizer', 'asset-manifest.json'), 'r') as z4man:
      gfxfiles = list(filter(lambda f: f.endswith('.bin'), json.load(z4man)['files'].values()))
      for gfxfile in gfxfiles:
        name = re.match(r'\.\/static\/media\/Graphics(\w+)\.[a-f0-9]{8}\.bin', gfxfile).group(1)
        path = os.path.join('Z4Randomizer', gfxfile[2:].replace('/', os.path.sep))
        gfxopt['choices'].append({ 'text': name, 'value': path })
    self.base_gfx_count = len(gfxopt['choices'])  # TODO: Use these to block sharing settings codes if using non-base sprites
    if os.path.isdir('sprites'):
      customs = list(filter(lambda f: f.endswith('.bin'), os.listdir('sprites')))
      for custom in customs:
        name = re.match(r'(\w+).*\.bin', custom).group(1)
        if any(map(lambda c: c['text'] == name, gfxopt['choices'])):
          name += '*'
        gfxopt['choices'].append({ 'text': name, 'value': os.path.join('sprites', custom) })

    self.input_label = tk.Label(self, text='Input Filename (US 1.0 ROM):', justify='left')
    self.input_label.grid(row=0, column=0, sticky=tk.E, padx='2m', pady='1m')
    self.input_entry = tk.Entry(self)
    self.input_entry.grid(row=0, column=1, sticky=tk.E+tk.W, padx='1m')
    self.input_button = tk.Button(self, text='...', justify='left', command=self.select_input)
    self.input_button.grid(row=0, column=2, padx='2m')

    self.globals_frame = tk.Frame(self)
    self.create_global_frame()
    self.globals_frame.grid(row=1, column=0, columnspan=3)
    self.create_player_frame(0)
    self.notebook.grid(row=2, column=0, columnspan=3)

    button_frame = tk.Frame(self)
    self.generate_button = tk.Button(button_frame, text='Generate!', command=self.generate_seed)
    self.generate_button.grid(row=0, column=0, pady='1m')
    button_frame.grid(row=3, column=0, columnspan=3)

  def add_to_frame(self, f, opt, x, y, suff=''):
    tk.Label(f, text=opt['text']+':', justify='left').grid(row=y, column=x, sticky=tk.E, padx='2m', pady='1m')
    if opt['type'] == 'boolean':
      var = tk.IntVar(name=opt['arg']+suff)
      var.set(opt['default'])
      opt['widget'] = tk.Checkbutton(f, variable=var, onvalue=1, offvalue=0)
      opt['widget'].var = var
      opt['widget'].grid(row=y, column=x+1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
    elif opt['type'] == 'string':
      var = tk.StringVar(name=opt['arg']+suff)
      var.set(opt['default'])
      opt['widget'] = tk.Entry(f, textvariable=var)
      opt['widget'].var = var
      opt['widget'].grid(row=y, column=x+1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
    elif opt['type'] == 'ff':
      var = tk.StringVar(name=opt['arg']+suff)
      var.set(opt['default'])
      opt['widget'] = tk.Spinbox(f, textvariable=var, from_=0.1, to=100.0, increment=0.1)
      opt['widget'].var = var
      opt['widget'].grid(row=y, column=x+1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
    elif opt['type'] == 'multi':
      var = tk.StringVar(name=opt['arg']+suff)
      var.set(opt['default'])
      opt['widget'] = ttk.Spinbox(f, textvariable=var, from_=1, to=8, increment=1, state='readonly', command=self.handle_multi)
      opt['widget'].var = var
      opt['widget'].grid(row=y, column=x+1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
      self.multi_widget = opt['widget']
    elif opt['type'] == 'choice':
      var = tk.StringVar(name=opt['arg']+suff)
      var.set([c['text'] for c in opt['choices'] if c['value'] == opt['default']][0])
      opt['widget'] = ttk.Combobox(f, textvariable=var, state='readonly', values=list(map(lambda c: c['text'], opt['choices'])))
      opt['widget'].var = var
      opt['widget'].grid(row=y, column=x+1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
    elif opt['type'] == 'file_out':
      pass  # TODO?
    elif opt['type'] == 'gfx':
      var = tk.StringVar(name=opt['arg']+suff)
      var.set([c['text'] for c in opt['choices'] if c['value'] == opt['default']][0])
      opt['widget'] = ttk.Combobox(f, textvariable=var, state='readonly', values=list(map(lambda c: c['text'], opt['choices'])))
      opt['widget'].var = var
      opt['widget'].grid(row=y, column=x+1, columnspan=2, sticky=tk.E+tk.W, padx='2m')

  def create_global_frame(self):
    f = self.globals_frame
    confnum = 0
    for opt in self.global_opts:
      g_row = confnum // UI_COLUMNS
      g_col = (confnum % UI_COLUMNS) * 3
      self.add_to_frame(f, opt, g_col, g_row)
      confnum += 1

  def create_player_frame(self, pnum):
    # Player 0 = Shared options
    # Player 1+ = Individual options
    f = self.frames[pnum]
    confnum = 0
    suff = str(pnum) if pnum > 0 else ''
    for opt in self.player_opts:
      g_row = confnum // UI_COLUMNS
      g_col = (confnum % UI_COLUMNS) * 3
      self.add_to_frame(f, opt, g_col, g_row, suff)
      confnum += 1

  def select_input(self):
    dialog_args = { 'filetypes': [('GBC ROM', '*.gbc')] }
    filename = askopenfilename(**dialog_args)
    if filename:
      filename = filename.replace('/', os.path.sep)
      self.input_entry.delete(0, tk.END)
      self.input_entry.insert(0, filename)

  def add_args(self, args, opts, suff=''):
    for opt in opts:
      if suff and self.getvar(opt['arg']) == self.getvar(opt['arg']+suff):
        # Do not add args for multiworld if they're the same as the shared arg
        continue
      val = self.getvar(opt['arg']+suff)
      if opt['type'] == 'boolean':
        if val:
          args.append('--' + opt['arg'])
      elif opt['type'] == 'string':
        if val:
          args.append('--' + opt['arg'] + '=' + val)
      elif opt['type'] == 'multi':
        ival = int(val)
        if ival > 1:
          args.append('--' + opt['arg'] + '=' + str(ival))
      elif opt['type'] == 'choice':
        argval = next(filter(lambda c: c['text'] == val, opt['choices']))['value']
        if argval:
          args.append('--' + opt['arg'] + '=' + argval)
      elif opt['type'] == 'gfx':
        argval = next(filter(lambda c: c['text'] == val, opt['choices']))['value']
        if argval != 'default':
          args.append('--' + opt['arg'] + '=' + argval)

  def generate_seed(self):
    args = []
    self.add_args(args, self.global_opts)
    self.add_args(args, self.player_opts)

    if self.multi > 1:
      for pnum in range(1, self.multi + 1):
        multi_args = []
        self.add_args(multi_args, self.player_opts, str(pnum))
        arg_string = ' '.join(multi_args)
        if '\\' in arg_string:
          arg_string = arg_string.replace('\\', '\\\\')
        args.append('--multiworld-config=' + arg_string)

    args.append(self.input_entry.get())
    ladxr.main(args)

  def handle_multi(self):
    val = int(self.multi_widget.get())
    if val > self.multi:
      if val == 2:
        self.frames.append(tk.Frame(self.notebook))
        self.notebook.add(self.frames[-1], text='Player 1')
        self.create_player_frame(1)
      self.frames.append(tk.Frame(self.notebook))
      self.notebook.add(self.frames[-1], text=f'Player {val}')
      self.create_player_frame(val)
    elif val < self.multi:
      self.notebook.forget(self.frames[-1])
      del self.frames[-1]
      if val == 1:
        self.notebook.forget(self.frames[-1])
        del self.frames[-1]
    self.multi = val

if __name__ == '__main__':
  root = tk.Tk()
  root.title('LADXR')
  ui = LadxrUi(master=root)
  ui.mainloop()
