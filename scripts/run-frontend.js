const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function runNpm(args, cwd) {
  const cmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
  const res = spawnSync(cmd, args, { cwd, stdio: 'inherit' });
  if (res.error) {
    console.error(res.error);
    process.exit(1);
  }
  process.exit(res.status || 0);
}

const action = process.argv[2];
const repoRoot = path.resolve(__dirname, '..');
const frontendPath = path.join(repoRoot, 'task-manager', 'frontend');

if (!fs.existsSync(frontendPath)) {
  console.log(`no frontend to ${action} at ${frontendPath}`);
  process.exit(0);
}

if (action === 'install') {
  runNpm(['install'], frontendPath);
} else if (action === 'build') {
  runNpm(['run', 'build'], frontendPath);
} else if (action === 'dev') {
  runNpm(['run', 'dev'], frontendPath);
} else if (action === 'preview') {
  runNpm(['run', 'preview'], frontendPath);
} else {
  console.error('Unknown action. Use: install | build | dev | preview');
  process.exit(1);
}
