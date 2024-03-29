# Simple ruby 1.9.3 spec.
# Note:
#It does not installs ruby tk bindings
#It does not follows Fedora Packaging Guidelines:
#https://fedoraproject.org/wiki/Packaging:Ruby
#It requires libyaml 0.1.4 which is not included in fedora 15 repocitories

%global	rubyxver	1.9
%global	rubyver	1.9.3
%global	_patchlevel	0
%global	dotpatchlevel	%{?_patchlevel:.%{_patchlevel}}
%global	patchlevel	%{?_patchlevel:-p%{_patchlevel}}
%global	arcver		%{rubyver}%{?patchlevel}

Name:           ruby
Version:        %{rubyver}%{?dotpatchlevel}
Release:        1%{?dist}
License:        Ruby or 2-clause BSDL
URL:            http://www.ruby-lang.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gdbm-devel
BuildRequires: ncurses-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: readline-devel

#requires libyaml-devel 0.1.4
BuildRequires: libyaml-devel >= 0.1.4

# I removeve tk
#BuildRequires: tk-devel

Source0:        ftp://ftp.ruby-lang.org/pub/ruby/%{name}/%{rubyxver}/%{name}-%{arcver}.tar.gz
Summary:        An interpreter of object-oriented scripting language
Group:          Development/Languages

Provides:       ruby(abi) = %{rubyxver}
Provides:       ruby-irb = %{version}-%{release}
Provides:       ruby-rdoc = %{version}-%{release}
Provides:       ruby-libs = %{version}-%{release}
Provides:       ruby-ri = %{version}-%{release}
Provides:       ruby-devel

Obsoletes:      ruby-libs < %{version}-%{release}
Obsoletes:      ruby-irb < %{version}-%{release}
Obsoletes:      ruby-rdoc < %{version}-%{release}
Obsoletes:      ruby-ri < %{version}-%{release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -n %{name}-%{arcver}

%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"

# configure options
#  --disable-rpath \         embed run path into extension libraries
#  --enable-shared \         build a shared library for Ruby
#  --disable-install-doc \   do not install neither rdoc indexes nor C API documents during install
#  --disable-install-rdoc \  do not install rdoc indexes during install
#  --disable-install-capi \  do not install C API documents during install
#  --without-X11 \           do not install X11. Tk requires X11 
#  --without-tk \            do not install tk. I do not have tk on a server

# Iremoved tk / X11
%configure \
  --disable-rpath \
  --enable-shared \
  --with-out-ext=tk \
  --includedir=%{_includedir}/ruby \
  --libdir=%{_libdir}

make %{?_smp_mflags}

%install
# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT

#we don't want to keep the src directory
rm -rf $RPM_BUILD_ROOT/usr/src

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}
%{_includedir}
%{_datadir}
%{_libdir}
