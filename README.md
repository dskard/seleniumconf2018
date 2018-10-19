# seleniumconf2018-chicago
Talk proposal and materials for SeleniumConf 2018 in Chicago, USA

## Jumping Starting an Organization's Testing with Selenium Grid Docker Containers, Selene, and pytest

Between new browser version, Selenium plugins, and differences in developer's
systems, supporting a setup that runs locally and also translates to CI can be
difficult. Before you roll your own solution, check out this configuration that
lets you focus on what you really care about: writing tests!


### Description

Setting up your Selenium based test infrastructure shouldn't be a hassle, but with constantly updating web browser versions, external Selenium browser plugins, and differences in developer's operating systems, supporting a setup that your team can run locally and also translates to a continuous integration system can make you want to pull out your hair. Before you jump into rolling your own solution, check out this configuration that uses tools maintained by Open Source projects and lets you focus on the part of testing you really care about: writing the tests!

In this talk I'll introduce a setup based on the Selenium Project's Selenium Grid Docker images, a Python library named Selene, and the  pytest framework that is easy to maintain, version, upgrade, and distribute to members of your development team. It lowers the barriers to getting started writing Selenium tests and grows with your organization to allow for complex configurations and testing scenarios.

### Presentations

[Google Slides]()
[PDF Slides]()
[PDF Slides with notes]()

### Example template

This repositories `template` directory holds example files you can run on your
own computer. To get started, make sure you have the following software on your
computer:
  * bash
  * coreutils (id, rm, cd, cat, printf, ...)
  * docker
  * docker-compose
  * git
  * make
  * python 2.7+
  * vncviewer (macosx users can launch vnc from spotlight, or the ```open```
    command in the terminal)

Then, clone this repository:

```
git clone https://github.com/dskard/seleniumconf2018.git dskard-seleniumconf2018;
cd dskard-seleniumconf2018;
```

And run these three commands:
```
make test-env-up
make test
make test-env-down
```

You can use the `shownode` script to view the test cases as they run:
```
make test-env-up
./shownode
make test
make test-env-down
```

Read more about the template
