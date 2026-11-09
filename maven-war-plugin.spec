Name:		maven-war-plugin
Version:	3.5.1
Release:	1
Summary:	Builds a web application archive from a Maven project
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/plugins/maven-war-plugin/
Source0:	https://github.com/apache/maven-war-plugin/archive/refs/tags/maven-war-plugin-%{version}.tar.gz#/maven-war-plugin-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
# Generates META-INF/maven/plugin.xml. The separate annotations package
# conflicts with maven-components on the same index file.
BuildRequires:	maven-plugin-tools >= 3.16.0
BuildRequires:	mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:	mvn(org.apache.maven:maven-archiver)
BuildRequires:	maven-archiver >= 3.6.6
Requires:	maven-archiver >= 3.6.6
BuildRequires:	mvn(org.apache.maven.shared:maven-filtering)
BuildRequires:	maven-filtering >= 3.5.1
Requires:	maven-filtering >= 3.5.1
BuildRequires:	mvn(org.apache.maven.shared:maven-mapping)
BuildRequires:	maven-mapping >= 3.0.0
Requires:	maven-mapping >= 3.0.0
BuildRequires:	mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:	maven-shared-utils >= 3.5.0
Requires:	maven-shared-utils >= 3.5.0
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	apache-commons-io >= 1:2.22.0
Requires:	apache-commons-io >= 1:2.22.0
BuildRequires:	mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:	plexus-archiver >= 4.15.0
Requires:	plexus-archiver >= 4.15.0
BuildRequires:	mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:	plexus-interpolation >= 1.30.0
Requires:	plexus-interpolation >= 1.30.0
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.apache.maven:maven-plugin-api)
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven:maven-artifact)
BuildRequires:	mvn(org.apache.maven:maven-model)
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
Requires:	javax.inject >= 1-2
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven2-plugin-war <= 0:2.0.8
Provides:	maven2-plugin-war = %{EVRD}
Obsoletes:	maven-war-plugin-javadoc < %{EVRD}

%description
Assembles a WAR from classes, web resources, and dependency jars.
3.5.1 is the current stable release. Overlays, filtering, and the
archive layout come from the system jars. Tests need JUnit Jupiter,
so they are not run.

%prep
%autosetup -n maven-war-plugin-maven-war-plugin-%{version}
rm -rf src/test src/it .github Jenkinsfile
python - <<'PY'
import xml.etree.ElementTree as ET

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.plugins")
add(root, "artifactId", "maven-war-plugin")
add(root, "version", "%{version}")
add(root, "packaging", "maven-plugin")
add(root, "name", "Apache Maven WAR Plugin")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
items = (
    ("org.apache.maven", "maven-archiver", "3.6.6", None),
    ("org.apache.maven.shared", "maven-filtering", "3.5.1", None),
    ("org.apache.maven.shared", "maven-mapping", "3.0.0", None),
    ("org.apache.maven.shared", "maven-shared-utils", "3.5.0", None),
    ("commons-io", "commons-io", "2.22.0", None),
    ("org.codehaus.plexus", "plexus-archiver", "4.15.0", None),
    ("org.codehaus.plexus", "plexus-interpolation", "1.30.0", None),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", None),
    ("org.apache.maven", "maven-plugin-api", "3.10.0", "provided"),
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven", "maven-artifact", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model", "3.10.0", "provided"),
    ("javax.inject", "javax.inject", "1", "provided"),
    ("org.apache.maven.plugin-tools", "maven-plugin-annotations", "3.15.2", "provided"),
)
for group, artifact, version, scope in items:
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
build = ET.SubElement(root, tag("build"))
plugins = ET.SubElement(build, tag("plugins"))
plugin = ET.SubElement(plugins, tag("plugin"))
add(plugin, "groupId", "org.apache.maven.plugins")
add(plugin, "artifactId", "maven-plugin-plugin")
add(plugin, "version", "3.16.0")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE README.md
