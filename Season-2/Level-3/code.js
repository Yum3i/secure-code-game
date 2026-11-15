// Welcome to Secure Code Game Season-2/Level-3!

// Follow the instructions below to get started:

// 1. test.js is passing but the code here is vulnerable
// 2. Review the code. Can you spot the bugs(s)?
// 3. Fix the code.js but ensure that test.js passes
// 4. Run hack.js and if passing then CONGRATS!
// 5. If stuck then read the hint
// 6. Compare your solution with solution.js

const express = require("express");
const bodyParser = require("body-parser");
const libxmljs = require("libxmljs");
const app = express();

app.use(bodyParser.json());
app.use(bodyParser.text({ type: "application/xml" }));

// The /ufo/upload endpoint was removed: it saved any file under any name
// (including "../" paths and ".admin" files) and nothing in the app needs it.

app.post("/ufo", (req, res) => {
  const contentType = req.headers["content-type"];

  if (contentType === "application/json") {
    console.log("Received JSON data:", req.body);
    res.status(200).json({ ufo: "Received JSON data from an unknown planet." });
  } else if (contentType === "application/xml") {
    // DTDs and entities are not needed for UFO data, but they allow XXE
    // (reading server files) and "billion laughs" attacks, so they are rejected
    if (typeof req.body !== "string" || /<!(DOCTYPE|ENTITY)/i.test(req.body)) {
      return res.status(400).set("Content-Type", "text/plain").send("Invalid XML");
    }

    try {
      const xmlDoc = libxmljs.parseXml(req.body, {
        replaceEntities: false, // never substitute entities
        recover: false, // broken XML is an error, not something to guess
        nonet: true, // never load anything from the network
      });

      const root = xmlDoc.root();
      if (!root) {
        return res.status(400).set("Content-Type", "text/plain").send("Invalid XML");
      }

      const extractedContent = [];
      root.childNodes().forEach((node) => {
        if (node.type() === "element") {
          extractedContent.push(node.text());
        }
      });

      // The hidden "admin" feature that ran XML content as shell commands
      // was removed: it gave anyone remote command execution on the server.

      res
        .status(200)
        .set("Content-Type", "text/plain")
        .send(extractedContent.join(" "));
    } catch (error) {
      console.error("XML parsing or validation error:", error.message);
      // the parser's error text is not sent back to the client
      res.status(400).set("Content-Type", "text/plain").send("Invalid XML");
    }
  } else {
    res.status(405).send("Unsupported content type");
  }
});

const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

module.exports = server;