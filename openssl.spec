# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
%define soversion 10

# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

Summary: A general purpose cryptography library with TLS implementation
Name: openssl
Version: 1.0.0c
Release: 1
# We remove certain patented algorithms from the openssl source tarball
# with the hobble-openssl script which is included below.
Source: openssl-%{version}-usa.tar.bz2
Source1: hobble-openssl
Source2: Makefile.certificate
Source6: make-dummy-cert
Source8: openssl-thread-test.c
Source9: opensslconf-new.h
Source10: opensslconf-new-warning.h
# Build changes
Patch0: openssl-1.0.0-beta4-redhat.patch
Patch1: openssl-1.0.0-beta3-defaults.patch
Patch3: openssl-1.0.0-beta3-soversion.patch
Patch4: openssl-1.0.0-beta5-enginesdir.patch
Patch5: openssl-0.9.8a-no-rpath.patch
Patch6: openssl-0.9.8b-test-use-localhost.patch
Patch7: openssl-1.0.0-timezone.patch
Patch8: openssl-1.0.0c-remove-date-string.patch
# Bug fixes
Patch23: openssl-1.0.0-beta4-default-paths.patch
Patch24: openssl-0.9.8j-bad-mime.patch
Patch25: openssl-1.0.0a-manfix.patch
# Functionality changes
Patch32: openssl-0.9.8g-ia64.patch
Patch33: openssl-1.0.0-beta4-ca-dir.patch
Patch34: openssl-0.9.6-x509.patch
Patch35: openssl-0.9.8j-version-add-engines.patch
Patch38: openssl-1.0.0-beta5-cipher-change.patch
Patch39: openssl-1.0.0b-ipv6-apps.patch
Patch40: openssl-1.0.0a-fips.patch
Patch41: openssl-1.0.0-beta3-fipscheck.patch
Patch43: openssl-1.0.0a-fipsmode.patch
Patch44: openssl-1.0.0-beta3-fipsrng.patch
Patch45: openssl-0.9.8j-env-nozlib.patch
Patch47: openssl-1.0.0-beta5-readme-warning.patch
Patch49: openssl-1.0.0-beta4-algo-doc.patch
Patch50: openssl-1.0.0-beta4-dtls1-abi.patch
Patch51: openssl-1.0.0c-version.patch
Patch52: openssl-1.0.0b-aesni.patch
Patch53: openssl-1.0.0-name-hash.patch
# Backported fixes including security fixes
Patch101: openssl-1.0.0c-CVE-2011-0014.patch

License: OpenSSL
Group: System/Libraries
URL: http://www.openssl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: mktemp,  perl, sed, zlib-devel, diffutils, util-linux
Requires: mktemp
#Requires: ca-certificates >= 2008-5

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name} = %{version}-%{release},  zlib-devel
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: %{name} = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q

chmod +x %{SOURCE1}
%{SOURCE1} > /dev/null
%patch0 -p1 -b .redhat
%patch1 -p1 -b .defaults
%patch3 -p1 -b .soversion
%patch4 -p1 -b .enginesdir
%patch5 -p1 -b .no-rpath
%patch6 -p1 -b .use-localhost
%patch7 -p1 -b .timezone
%patch8 -p1 -b .remove-date-string

%patch23 -p1 -b .default-paths
%patch24 -p1 -b .bad-mime
%patch25 -p1 -b .manfix

%patch32 -p1 -b .ia64
%patch33 -p1 -b .ca-dir
%patch34 -p1 -b .x509
%patch35 -p1 -b .version-add-engines
%patch38 -p1 -b .cipher-change
%patch39 -p1 -b .ipv6-apps
%patch40 -p1 -b .fips
%patch41 -p1 -b .fipscheck
%patch43 -p1 -b .fipsmode
%patch44 -p1 -b .fipsrng
%patch45 -p1 -b .env-nozlib
%patch47 -p1 -b .warning
%patch49 -p1 -b .algo-doc
%patch50 -p1 -b .dtls1-abi
%patch51 -p1 -b .version
%patch52 -p1 -b .aesni
%patch53 -p1 -b .name-hash

%patch101 -p0 -b .CVE-2011-0014

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build 
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_arch}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux-s390x"
%endif
%ifarch %{arm} sh3 sh4
sslarch=linux-generic32
%endif
# ia64, x86_64, ppc, ppc64 are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
	enable-cms enable-md2 no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa \
	--enginesdir=%{_libdir}/openssl/engines \
	shared ${sslarch} fips

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack"
make depend
make all

# Generate hashes for the included certs.
make rehash

# Verify that what was compiled actually works.
# We must revert patch33 before tests otherwise they will fail
patch -p1 -R < %{PATCH33}

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
make -C test apps tests
%{__cc} -o openssl-thread-test \
	-I./include \
	$RPM_OPT_FLAGS \
	%{SOURCE8} \
	-L. \
	-lssl -lcrypto \
	-lpthread -lz -ldl
./openssl-thread-test --threads %{thread_test_threads}

# Add generation of HMAC checksum of the final stripped library
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    crypto/fips/fips_standalone_sha1 $RPM_BUILD_ROOT/%{_lib}/libcrypto.so.%{version} >$RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{version}.hmac \
    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{soversion}.hmac \
    crypto/fips/fips_standalone_sha1 $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.hmac \
    ln -sf .libssl.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.hmac \
%{nil}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs
mv $RPM_BUILD_ROOT%{_libdir}/engines $RPM_BUILD_ROOT%{_libdir}/openssl
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man/* $RPM_BUILD_ROOT%{_mandir}/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
mkdir $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} $RPM_BUILD_ROOT/%{_lib}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done
for lib in $RPM_BUILD_ROOT/%{_lib}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f ../../%{_lib}/`basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT/%{_lib}/`basename ${lib} .%{version}`.%{soversion}
done

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/make-dummy-cert

# Make sure we actually include the headers we built against.
for header in $RPM_BUILD_ROOT%{_includedir}/openssl/* ; do
	if [ -f ${header} -a -f include/openssl/$(basename ${header}) ] ; then
		install -m644 include/openssl/`basename ${header}` ${header}
	fi
done

# Rename man pages so that they don't conflict with other system man pages.
pushd $RPM_BUILD_ROOT%{_mandir}
for manpage in man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done
for conflict in passwd rand ; do
	rename ${conflict} ssl${conflict} man*/${conflict}*
done
popd

# Pick a CA script.
pushd  $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc
mv CA.sh CA
popd

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the openssl.cnf timestamp is identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif
%ifarch sparc64
basearch=sparc64
%endif

%ifarch %{multilib_arches}
# Do an opensslconf.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
install -m644 %{SOURCE10} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
cat $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h >> \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
install -m644 %{SOURCE9} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h
%endif

# Remove unused files from upstream fips support
rm -rf $RPM_BUILD_ROOT/%{_bindir}/openssl_fips_fingerprint
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fips_premain.*
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fipscanister.*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc FAQ LICENSE CHANGES NEWS INSTALL README
%doc doc/c-indentation.el doc/openssl.txt
%doc doc/openssl_button.html doc/openssl_button.gif
%doc doc/ssleay.txt
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%{_sysconfdir}/pki/tls/certs/make-dummy-cert
%{_sysconfdir}/pki/tls/certs/Makefile
%dir %{_sysconfdir}/pki/tls/misc
%{_sysconfdir}/pki/tls/misc/CA
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts
%{_sysconfdir}/pki/tls/misc/c_*
%{_sysconfdir}/pki/tls/private

%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf

%attr(0755,root,root) %{_bindir}/openssl
%attr(0755,root,root) /%{_lib}/libcrypto.so.%{version}
%attr(0755,root,root) /%{_lib}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%attr(0644,root,root) /%{_lib}/.libcrypto.so.*.hmac
%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac
%attr(0755,root,root) %{_libdir}/openssl
%attr(0644,root,root) %{_mandir}/man1*/[ABD-Zabcd-z]*
%attr(0644,root,root) %{_mandir}/man5*/*
%attr(0644,root,root) %{_mandir}/man7*/*

%files devel
%defattr(-,root,root)
%{_prefix}/include/openssl
%attr(0644,root,root) %{_libdir}/*.a
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_mandir}/man3*/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files perl
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/c_rehash
%attr(0644,root,root) %{_mandir}/man1*/*.pl*
%{_sysconfdir}/pki/tls/misc/*.pl
%{_sysconfdir}/pki/tls/misc/tsget

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

