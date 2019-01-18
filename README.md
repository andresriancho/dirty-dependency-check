## Dirty dependency check

This tool will parse a `pom.xml` file, extract all dependencies, and check them
against NIST's vulnerability database.

[OWASP Dependency Check](https://github.com/jeremylong/DependencyCheck) requires
you to be able to build the project maven project, dirty dependency check will work
even when some dependencies are missing (ie. they are in a private repository).

## Disclaimer

This tool is not a replacement for [OWASP Dependency Check](https://github.com/jeremylong/DependencyCheck),
just a hack to make my life easier during Java application security assessments.

## Dependencies

 * Maven (`apt-get install maven`)
 
## Run

```
python dependency-check.py --pom=~/current-project/src/pom.xml --output=vulnerabilities.json
```

## Updating the NIST DB

```
git clone https://github.com/stevespringett/nist-data-mirror.git
cd nist-data-mirror
mvn clean package
cd target
rm -rf mirror/*
mkdir -p mirror
java -jar nist-data-mirror.jar mirror json
cp mirror/*.json.gz ../../dirty-dependency-check/data/
```
