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
from tkinter import ttk
from tkinter.filedialog import askopenfilename

class LadxrUi(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()

    self.ladxr_opts = [
      { 'text': 'Race Mode', 'arg': 'race', 'type': 'boolean', 'default': True },
      { 'text': 'Spoiler Format', 'arg': 'spoilerformat', 'type': 'choice', 'choices': [
        { 'text': 'None', 'value': 'none' },
        { 'text': 'Console', 'value': 'console' },
        { 'text': 'Text', 'value': 'text' },
        { 'text': 'JSON', 'value': 'json' }
      ], 'default': 'none' },
      { 'text': 'Seed', 'arg': 'seed', 'type': 'string', 'default': '' },
      { 'text': 'Randomize Heart Pieces', 'arg': 'heartpiece', 'type': 'boolean', 'default': True },
      { 'text': 'Randomize Seashells', 'arg': 'seashells', 'type': 'boolean', 'default': True },
      { 'text': 'Keysanity', 'arg': 'keysanity', 'type': 'boolean', 'default': False },
      { 'text': 'Randomize Heart Containers', 'arg': 'heartcontainers', 'type': 'boolean', 'default': False },
      { 'text': 'Randomize Witch', 'arg': 'witch', 'type': 'boolean', 'default': True },
      { 'text': 'Add items to owl statues', 'arg': 'owlstatues', 'type': 'choice', 'choices': [
        { 'text': 'Never', 'value': 'none' },
        { 'text': 'Dungeons', 'value': 'dungeon' },
        { 'text': 'Overworld', 'value': 'overworld' },
        { 'text': 'Dungeons and Overworld', 'value': 'both' }
      ], 'default': 'none' },
      { 'text': 'Dungeon Shuffle', 'arg': 'dungeonshuffle', 'type': 'boolean', 'default': False },
      { 'text': 'Boss Shuffle', 'arg': 'bossshuffle', 'type': 'boolean', 'default': False},
      { 'text': 'Boomerang Mode', 'arg': 'boomerang', 'type': 'choice', 'choices': [
        { 'text': 'Normal (require lens)', 'value': 'default' },
        { 'text': 'Trade', 'value': 'trade' },
        { 'text': 'Gift', 'value': 'gift' }
      ], 'default': 'default' },
      { 'text': 'Bow Wow Mode', 'arg': 'bowwow', 'type': 'choice', 'choices': [
        { 'text': 'Disabled', 'value': 'normal' },
        { 'text': 'Enabled', 'value': 'always' },
        { 'text': 'Swordless', 'value': 'swordless' },
      ], 'default': 'normal' },
      { 'text': 'Logic', 'arg': 'logic', 'type': 'choice', 'choices': [
        { 'text': 'Normal', 'value': 'normal' },
        { 'text': 'Hard', 'value': 'hard' },
        { 'text': 'Glitched', 'value': 'glitched' },
        { 'text': 'Hell', 'value': 'hell' }
      ], 'default': 'normal' },
      { 'text': 'Instruments Required', 'arg': 'goal', 'type': 'choice', 'choices': [
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
        { 'text': 'Random', 'value': 'random' }
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
        { 'text': 'Start with 1 heart', 'value': '1' }
      ], 'default': 'default' },
      { 'text': 'Oracles Mode', 'arg': 'hard-mode', 'type': 'boolean', 'default': False},
      { 'text': 'Stealing', 'arg': 'steal', 'type': 'choice', 'choices': [
        { 'text': 'Always', 'value': 'always' },
        { 'text': 'Never', 'value': 'never' },
        { 'text': 'Normal', 'value': 'default' }
      ], 'default': 'always' },
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
      # This default differs from web because speedbois will want Flock clips
      { 'text': 'Nag Messages', 'arg': 'nag-messages', 'type': 'boolean', 'default': True },
      { 'text': 'Sprites', 'arg': 'gfxmod', 'type': 'gfx', 'choices': [{ 'text': 'Default', 'value': 'default' }], 'default': 'default' },
      
      # TODO: Not sure what values are used, will check with Daid before adding
      # { 'text': 'Tunic Palette', 'arg': 'linkspalette', 'type': 'choice' }
    ]

    with open(os.path.join('Z4Randomizer', 'asset-manifest.json'), 'r') as z4man:
      gfxfiles = list(filter(lambda f: f.endswith('.bin'), json.load(z4man)['files'].values()))
      gfxopt = self.ladxr_opts[-1]
      for gfxfile in gfxfiles:
        name = re.match(r'\.\/static\/media\/Graphics(\w+)\.[a-f0-9]{8}\.bin', gfxfile).group(1)
        path = os.path.join('Z4Randomizer', gfxfile[2:].replace('/', os.path.sep))
        gfxopt['choices'].append({ 'text': name, 'value': path })

    row = 0
    self.input_label = tk.Label(self, text='Input Filename (US 1.0 ROM):', justify='left')
    self.input_label.grid(row=row, column=0, sticky=tk.E, padx='2m', pady='1m')
    self.input_entry = tk.Entry(self)
    self.input_entry.grid(row=row, column=1, sticky=tk.E+tk.W, padx='1m')
    self.input_button = tk.Button(self, text='...', justify='left', command=self.select_input)
    self.input_button.grid(row=row, column=2, padx='2m')

    row += 1
    for opt in self.ladxr_opts:
      tk.Label(self, text=opt['text']+':', justify='left').grid(row=row, column=0, sticky=tk.E, padx='2m', pady='1m')
      if opt['type'] == 'boolean':
        var = tk.IntVar(name=opt['arg'])
        var.set(opt['default'])
        opt['widget'] = tk.Checkbutton(self, variable=var, onvalue=1, offvalue=0)
        opt['widget'].var = var
        opt['widget'].grid(row=row, column=1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
      elif opt['type'] == 'string':
        var = tk.StringVar(name=opt['arg'])
        var.set(opt['default'])
        opt['widget'] = tk.Entry(self, textvariable=var)
        opt['widget'].var = var
        opt['widget'].grid(row=row, column=1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
      elif opt['type'] == 'choice':
        var = tk.StringVar(name=opt['arg'])
        var.set([c['text'] for c in opt['choices'] if c['value'] == opt['default']][0])
        opt['widget'] = ttk.Combobox(self, textvariable=var, state='readonly', values=list(map(lambda c: c['text'], opt['choices'])))
        opt['widget'].var = var
        opt['widget'].grid(row=row, column=1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
      elif opt['type'] == 'file_out':
        pass  # TODO?
      elif opt['type'] == 'gfx':
        var = tk.StringVar(name=opt['arg'])
        var.set([c['text'] for c in opt['choices'] if c['value'] == opt['default']][0])
        opt['widget'] = ttk.Combobox(self, textvariable=var, state='readonly', values=list(map(lambda c: c['text'], opt['choices'])))
        opt['widget'].var = var
        opt['widget'].grid(row=row, column=1, columnspan=2, sticky=tk.E+tk.W, padx='2m')
      row += 1

    self.generate_button = tk.Button(self, text='Generate!', command=self.generate_seed)
    self.generate_button.grid(row=row, column=0, columnspan=3, pady='1m')

  def select_input(self):
    dialog_args = { 'filetypes': [('GBC ROM', '*.gbc')] }
    filename = askopenfilename(**dialog_args)
    if filename:
      filename = filename.replace('/', os.path.sep)
      self.input_entry.delete(0, tk.END)
      self.input_entry.insert(0, filename)

  def generate_seed(self):
    args = []

    for opt in self.ladxr_opts:
      val = self.getvar(opt['arg'])
      if opt['type'] == 'boolean':
        if val:
          args.append('--' + opt['arg'])
      elif opt['type'] == 'string':
        if val:
          args.append('--' + opt['arg'] + '=' + val)
      elif opt['type'] == 'choice':
        argval = next(filter(lambda c: c['text'] == val, opt['choices']))['value']
        args.append('--' + opt['arg'] + '=' + argval)
      elif opt['type'] == 'gfx':
        argval = next(filter(lambda c: c['text'] == val, opt['choices']))['value']
        if argval != 'default':
          args.append('--' + opt['arg'] + '=' + argval)

    args.append(self.input_entry.get())
    ladxr.main(args)

if __name__ == '__main__':
  root = tk.Tk()
  root.title('LADXR')
  ui = LadxrUi(master=root)
  ui.mainloop()
