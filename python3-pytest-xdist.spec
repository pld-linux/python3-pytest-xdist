#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# tests [ptys needed]

Summary:	py.test distributed testing plugin
Summary(pl.UTF-8):	Wtyczka py.test do testów rozproszonych
Name:		python3-pytest-xdist
Version:	3.7.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-xdist/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-xdist/pytest_xdist-%{version}.tar.gz
# Source0-md5:	94bf52c692963572d85150770b6d234c
URL:		https://github.com/pytest-dev/pytest-xdist
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:77.0
BuildRequires:	python3-setuptools_scm >= 6.2.3
%if %{with tests}
BuildRequires:	python3-execnet >= 2.1
BuildRequires:	python3-filelock
BuildRequires:	python3-pytest >= 7.0.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pytest-xdist plugin extends py.test with some unique test
execution modes, like parallelization.

%description -l pl.UTF-8
Wtyczka pytest-xdist rozszerza py.test o kilka unikatowych
trybów wykonywania testów, jak choćby zrównoleglenie.

%package apidocs
Summary:	API documentation for Python pytest-xdist module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-xdist
Group:		Documentation

%description apidocs
API documentation for Python pytest-xdist module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-xdist.

%prep
%setup -q -n pytest_xdist-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=xdist.plugin,xdist.looponfail \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest testing
%endif

%if %{with doc}
sphinx-build -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst example/boxed.txt
%{py3_sitescriptdir}/xdist
%{py3_sitescriptdir}/pytest_xdist-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
