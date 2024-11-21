const fs = require("fs").promises;
const { customAlphabet } = require("nanoid");

const ID_LENGTH = 35;

function getNanoid() {
  const alphabet =
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

  const nanoid = customAlphabet(alphabet, ID_LENGTH);

  return nanoid();
}

const main = () => {
  const nanoid = getNanoid();

  fs.mkdir(nanoid)
    .then(() => {
      return Promise.all([
        fs.mkdir(`${nanoid}/en`),
      ]);
    })
    .then(() => {
      const properties = {
        numExercises: 0,
        estimatedCompletionTime: 0,
        author: "samus.io",
        authorGithubId: "samus-io"
      };

      fs.writeFile(`${nanoid}/properties.json`, JSON.stringify(properties, null, 2));
      fs.writeFile(`${nanoid}/en/README.md`, `# TODO\n`);
    })
    .catch((err) => {
      console.error(err);
    });
};

main();

