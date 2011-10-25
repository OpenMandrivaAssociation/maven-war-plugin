Name:           maven-war-plugin
Version:        2.1.1
Release:        3
Summary:        Maven WAR Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-war-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch: noarch

# Basic stuff
BuildRequires: jpackage-utils
BuildRequires: java-devel >= 0:1.6.0
# Maven and its dependencies
BuildRequires: maven
BuildRequires: maven-plugin-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-doxia
BuildRequires: maven-doxia-tools
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-surefire-plugin
BuildRequires: maven-plugin-cobertura
BuildRequires: maven-shared-filtering
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-idea-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-changes-plugin
BuildRequires: maven-invoker-plugin
# Others
BuildRequires: xstream

Requires: java
Requires: maven2
Requires: xstream
Requires: jpackage-utils
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

Provides:       maven2-plugin-war = 0:%{version}-%{release}
Obsoletes:      maven2-plugin-war <= 0:2.0.8

%description
Builds a Web Application Archive (WAR) file from the project output and its 
dependencies.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q 

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository

mvn-local -e \
        -Dmaven.test.skip=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

%add_to_maven_depmap org.apache.maven.plugins maven-war-plugin %{version} JPP maven-war-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

