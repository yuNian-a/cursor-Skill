#!/usr/bin/env node

const { installSkill, listSkills } = require('../lib/install');

const command = process.argv[2];
const skillName = process.argv[3];

async function main() {
  try {
    if (command === 'install' || command === 'i') {
      if (!skillName) {
        console.error('❌ 错误: 请指定要安装的 skill 名称');
        console.log('\n用法: npx @mierhaosi3/cursor-skills install <skill-name>');
        console.log('\n示例: npx @mierhaosi3/cursor-skills install news-agent-api');
        process.exit(1);
      }
      await installSkill(skillName);
    } else if (command === 'list' || command === 'ls') {
      await listSkills();
    } else if (command === 'help' || command === '--help' || command === '-h' || !command) {
      console.log(`
📦 Cursor Skills 安装工具

用法:
  npx @mierhaosi3/cursor-skills <command> [options]

命令:
  install <skill-name>  安装指定的 skill 到当前项目
  list                  列出所有可用的 skills
  help                  显示帮助信息

示例:
  npx @mierhaosi3/cursor-skills install news-agent-api
  npx @mierhaosi3/cursor-skills list

更多信息请访问: https://github.com/mierhaosi3/cursor-skills
      `);
    } else {
      console.error(`❌ 未知命令: ${command}`);
      console.log('使用 "npx @mierhaosi3/cursor-skills help" 查看帮助信息');
      process.exit(1);
    }
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();

