const test = require('node:test');
const assert = require('node:assert/strict');

const saved = new Map();
global.window = {};
global.localStorage = {
  getItem: (key) => saved.has(key) ? saved.get(key) : null,
  setItem: (key, value) => saved.set(key, value),
};
require('../frontend/games.js');

const samples = {
  numeric: {prompt:'Solve 3x + 5 = 20'},
  expression: {tiles:[2,3,4],operators:['+','*'],target:14},
  simulation: {mass:2,acceleration:3},
  circuit: {components:['battery','closed_switch','bulb']},
  atoms: {formula:'H2O'},
  reaction: {equation:'H₂ + O₂ → H₂O'},
  label: {diagram:'Plant cell',labels:['nucleus'],regions:['Center']},
  ecosystem: {species:['rabbits','foxes']},
  'code-edit': {task:'Repair the line',prompt:'return n % 2 == 1',tests:['even(2) → True']},
  order: {steps:['Set bounds','Compare midpoint']},
  'story-order': {blocks:['Plant seed','Flower blooms']},
  timeline: {events:[{name:'Moon landing',year:1969},{name:'Flight',year:1903}]},
  letters: {letters:'LPEPA',definition:'A fruit'},
  evidence: {scenario:'Why was a wall built?',evidence:['Raid report','Town map'],conclusions:['Defense','No evidence']},
  'map-click': {place:'Nile River region'},
  'region-order': {rule:'West to east',regions:['California','New York']},
  'output-predict': {prompt:'cout << 1',answer:'1'},
  'design-choice': {prompt:'Choose design',choices:['Interface','Global'],answer:0},
  'logic-builder': {prompt:'Build the condition',blocks:['x > 0','and','x < 4']},
  'structure-trace': {prompt:'Trace a stack',structure:'Stack',operations:['push(1)','pop()'],answer:[1]},
  'sql-query': {prompt:'Return all rows'},
  'er-diagram': {prompt:'Choose cardinality',choices:['1:N','M:N'],answer:0},
  'schedule': {prompt:'Schedule jobs',jobs:['A (3)','B (1)']},
  'memory-allocation': {prompt:'Allocate blocks',blocks:[100,200],requests:[50]},
  'route': {prompt:'Route packet',start:'A',end:'B',edges:[['A','B']]},
  'diagnose': {prompt:'Diagnose DNS',choices:['DNS','CPU'],answer:0},
  'ui-debug': {prompt:'Fix overflow',choices:['Fluid width','Fixed width'],answer:0},
};

test('every platform mechanic has a distinct interactive renderer', () => {
  for (const [mechanic, level] of Object.entries(samples)) {
    const game = {id:`test-${mechanic}`,title:mechanic,objective:'Test objective',instructions:'Test instructions',mechanic,level_count:1,levels:[level]};
    const html = window.PlatformGames.render(game,{level:0,score:0,mistakes:0,actions:0,complete:false},game.id);
    assert.match(html,/Test objective/,mechanic);
    assert.doesNotMatch(html,/undefined|null/,mechanic);
    assert.notEqual(html.indexOf('<button'),-1,mechanic);
  }
});

test('completed games show score and an explicit results action', () => {
  const game={id:'math-equation',title:'Equation Quest',objective:'Solve',instructions:'Enter x',mechanic:'numeric',level_count:2,levels:[{prompt:'x=1'},{prompt:'x=2'}]};
  const html=window.PlatformGames.render(game,{level:2,score:200,mistakes:1,actions:3,complete:true},'session-1');
  assert.match(html,/All levels complete/);
  assert.match(html,/View results/);
});
