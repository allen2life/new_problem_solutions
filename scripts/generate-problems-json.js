import ProblemManager from '../lib/problem.js';

function printHelp() {
  console.log(`Usage: node scripts/generate-problems-json.js [--help]

Generate the public problems JSON cache from the local problems/ directory.

Options:
  -h, --help   Show this help message
`);
}

if (process.argv.includes('-h') || process.argv.includes('--help')) {
  printHelp();
  process.exit(0);
}

const manager = new ProblemManager({ auto_load: false });

manager.init();
manager.save_problems();

console.log(`Generated problems.json with ${manager.getAll().length} problems.`);
