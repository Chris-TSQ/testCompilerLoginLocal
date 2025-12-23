const CompilerTestGenPlugin = require("./src/CompilerTestGenPlugin");

const filePath = process.argv[2];

try {
  const plugin = new CompilerTestGenPlugin({
    outputDir: "generated-tests"
  });

  plugin.run(filePath);
} catch (err) {
  console.error("ERROR:", err.message);
  process.exit(1);
}
