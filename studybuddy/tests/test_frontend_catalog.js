const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const extra = require('../frontend/legacy-game-content.js');
const rotating = require('../frontend/rotating-game-content.js');
const typing = require('../frontend/typing-programs.js');

const html = fs.readFileSync(path.join(__dirname, '..', 'frontend', 'index.html'), 'utf8');
const inline = html.match(/<script>\s*([\s\S]*?)<\/script>/)?.[1];
assert.ok(inline, 'main frontend script exists');
const start = inline.indexOf('const SUBJ=');
const end = inline.indexOf('const PLATFORM_GAMES=[]');
assert.ok(start >= 0 && end > start, 'frontend catalog initialization is present');
const expose = `
globalThis.__studyCatalog = {
  SUBJ, RAW, FCR, CODE, TYPE, FILL, Q, FC, GAMES, GM, gameContentCount,
  registerSubject, getDsaLanguage
};`;
const sandbox = { window: { STUDY_LEGACY_GAME_CONTENT: extra, STUDY_ROTATING_GAME_CONTENT: rotating, STUDY_TYPING_PROGRAMS: typing }, Object, Math, localStorage: { getItem: () => null } };
vm.runInNewContext(inline.slice(start, end) + expose, sandbox, { timeout: 3000 });
const catalog = sandbox.__studyCatalog;
const subjectItems = (subject, mode) => mode === 'quiz' || mode === 'chal' ? catalog.Q.filter(q => q.s === subject)
  : mode === 'flash' || mode === 'memory' ? catalog.FC.filter(c => c.s === subject)
  : mode === 'code' ? catalog.CODE.filter(q => q.s === subject)
  : mode === 'fill' ? catalog.FILL.filter(q => q.s === subject)
  : mode === 'typing' ? catalog.TYPE.filter(q => q.s === subject && (subject !== 'DSA' || q.language === catalog.getDsaLanguage())) : [];

test('every advertised legacy card resolves to its own populated mechanics bank', () => {
  assert.ok(catalog.GAMES.length >= 60);
  assert.equal(new Set(catalog.GAMES.map(game => game.id)).size, catalog.GAMES.length);
  for (const game of catalog.GAMES) {
    const items = subjectItems(game.s, game.m);
    assert.ok(items.length >= 4, `${game.id} has at least four playable items`);
    assert.equal(game.n, items.length, `${game.id} displays its actual content count`);
    assert.equal(catalog.GM[game.id].m, game.m, `${game.id} routes to the advertised mechanic`);
    assert.equal(new Set(items.map(item => item.id)).size, items.length, `${game.id} has distinct item IDs`);
  }
});

test('the complete inline frontend script parses', () => {
  assert.doesNotThrow(() => new vm.Script(inline, { filename: 'frontend/index.html inline script' }));
});

test('new local sessions rotate questions and never repeat a typing program immediately', () => {
  const start = inline.indexOf('function chooseFreshItems(');
  const end = inline.indexOf('\nfunction startG(', start);
  assert.ok(start >= 0 && end > start, 'local rotation helper exists');
  const storage = new Map();
  const context = {
    localStorage: {
      getItem: key => storage.get(key) ?? null,
      setItem: (key, value) => storage.set(key, value)
    },
    Math,
    JSON
  };
  vm.runInNewContext(`${inline.slice(start, end)}\nglobalThis.chooseFreshItems = chooseFreshItems;`, context);
  const bank = ['a', 'b', 'c', 'd', 'e', 'f'];
  const first = context.chooseFreshItems('quiz', bank, 4);
  const second = context.chooseFreshItems('quiz', bank, 4);
  assert.equal(first.length, 4);
  assert.equal(second.length, 4);
  assert.ok(new Set(second).size === 4);
  assert.ok(second.filter(id => !first.includes(id)).length >= 2);
  const programs = ['program-1', 'program-2', 'program-3', 'program-4'];
  const firstProgram = context.chooseFreshItems('typing', programs, 1)[0];
  const nextProgram = context.chooseFreshItems('typing', programs, 1)[0];
  assert.notEqual(nextProgram, firstProgram);
});

test('legacy quiz answers, fill-line exercises, code ordering, and typing prompts are valid', () => {
  for (const game of catalog.GAMES) {
    for (const item of subjectItems(game.s, game.m)) {
      if (game.m === 'quiz') {
        assert.ok(Array.isArray(item.o) && item.o.length >= 3, `${item.id} has answer options`);
        assert.ok(Number.isInteger(item.a) && item.a >= 0 && item.a < item.o.length, `${item.id} has a valid key`);
        assert.ok(item.x, `${item.id} explains its answer`);
      } else if (game.m === 'fill') {
        assert.ok(Array.isArray(item.o) && item.o.length >= 3, `${item.id} has line choices`);
        assert.ok(Number.isInteger(item.a) && item.a >= 0 && item.a < item.o.length, `${item.id} has a valid line answer`);
        assert.ok(item.x, `${item.id} explains the missing line`);
      } else if (game.m === 'code') {
        assert.equal(item.builder, true, `${item.id} is a code ordering task`);
        assert.ok(Array.isArray(item.parts) && item.parts.length >= 2, `${item.id} has reorderable code lines`);
      } else if (game.m === 'typing') {
        assert.ok(item.t.length >= 8, `${item.id} has a meaningful typing prompt`);
      } else if (game.m === 'flash' || game.m === 'memory') {
        assert.ok(item.f && item.b && item.f !== item.b, `${item.id} has a distinct concept and explanation`);
      }
    }
  }
});

test('teacher-added subjects receive playable quiz and recall banks instead of one-item placeholders', () => {
  catalog.registerSubject('TESTCOURSE', 'Test Course');
  for (const mode of ['quiz', 'flash', 'memory']) {
    const game = catalog.GAMES.find(item => item.id === `TESTCOURSE-${mode}`);
    assert.ok(game, `${mode} card registered`);
    assert.equal(game.n, 4);
    assert.equal(subjectItems('TESTCOURSE', mode).length, 4);
  }
});
