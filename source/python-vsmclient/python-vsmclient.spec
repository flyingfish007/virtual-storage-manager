%define version %{getenv:VERSION}
%define release %{getenv:RELEASE}

Name:             python-vsmclient
Version:          %{version}
Release:          %{release}
Summary:          Python API and CLI for vsm

Group:            Development/Languages
License:          Intel Reserved
URL:              http://intel.com/itflex
Source:           %{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python-prettytable
BuildRequires:    python-requests
BuildRequires:    python-simplejson
Requires:         python-httplib2
Requires:         python-prettytable
Requires:         python-setuptools

%description
This is a client for the vsm API. There's a Python API (the
vsmclient module), and a command-line script (vsm). Each implements
100% of the vsm API.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc LICENSE
%{_bindir}/vsm
%{python_sitelib}/vsmclient
%{python_sitelib}/*.egg-info
