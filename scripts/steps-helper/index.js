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
        fs.mkdir(`${nanoid}/es`),
        fs.mkdir(`${nanoid}/en`),
        fs.mkdir(`${nanoid}/docker`),
      ]);
    })
    .then(() => {
      fs.writeFile(`${nanoid}/es/README.md`, ``);
      fs.writeFile(`${nanoid}/en/README.md`, `# \n\n`);

      const properties = {
        numExercises: 0,
        estimatedCompletionTime: 0,
        author: "samus.io",
        authorGithubId: "samus-io"
      };

      fs.writeFile(`${nanoid}/properties.json`, JSON.stringify(properties, null, 2));
    })
    .catch((err) => {
      console.error(err);
    });
};

main();

