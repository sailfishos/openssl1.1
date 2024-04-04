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
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)

%define soversion 1.1
%define nofips 1
%define rname openssl

# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}
Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: %{rname}%{soversion}
Version: 1.1.1w
# Do not forget to bump SHLIB_VERSION on version upgrades
Release: 0

# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source: %{name}-%{version}.tar.gz
Source1: hobble-openssl
Source2: Makefile.certificate
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source9: opensslconf-new.h
Source10: opensslconf-new-warning.h
Source11: README.FIPS
Source12: ec_curve.c
Source13: ectest.c
Source14: fixpatch
# Build changes
Patch1: openssl-1.1.1-build.patch
Patch2: openssl-1.1.1-defaults.patch
Patch3: openssl-1.1.1-no-html.patch
Patch4: openssl-1.1.1-man-rename.patch
# Functionality changes
Patch31: openssl-1.1.1-conf-paths.patch
Patch32: openssl-1.1.1-version-add-engines.patch
Patch33: openssl-1.1.1-apps-dgst.patch
Patch36: openssl-1.1.1-no-brainpool.patch
Patch37: openssl-1.1.1-ec-curves.patch
Patch38: openssl-1.1.1-no-weak-verify.patch
Patch40: openssl-1.1.1-disable-ssl3.patch
Patch41: openssl-1.1.1-system-cipherlist.patch
Patch42: openssl-1.1.1-fips.patch
Patch44: openssl-1.1.1-version-override.patch
Patch45: openssl-1.1.1-weak-ciphers.patch
Patch46: openssl-1.1.1-seclevel.patch
Patch47: 0001-ts-Use-SHA256-instead-of-SHA1-and-SHA512-instead-MD5.patch
Patch48: openssl-1.1.1-fips-post-rand.patch
Patch49: openssl-1.1.1-evp-kdf.patch
Patch50: openssl-1.1.1-ssh-kdf.patch
Patch51: openssl-1.1.1-intel-cet.patch
Patch60: openssl-1.1.1-krb5-kdf.patch
Patch61: openssl-1.1.1-edk2-build.patch
Patch62: openssl-1.1.1-fips-curves.patch
Patch65: openssl-1.1.1-fips-drbg-selftest.patch
Patch66: openssl-1.1.1-fips-dh.patch
Patch67: openssl-1.1.1-kdf-selftest.patch
Patch69: openssl-1.1.1-alpn-cb.patch
Patch70: openssl-1.1.1-rewire-fips-drbg.patch
# Backported fixes including security fixes
Patch52: openssl-1.1.1-s390x-update.patch
Patch53: openssl-1.1.1-fips-crng-test.patch
Patch55: openssl-1.1.1-aes-asm-aesv8-armx.pl-20-improvement-on-ThunderX2.patch
Patch56: openssl-1.1.1-s390x-ecc.patch
Patch57: openssl-1_1-Optimize-RSA-armv8.patch
Patch58: openssl-1_1-Optimize-AES-GCM-uarchs.patch
Patch59: openssl-1_1-Optimize-AES-XTS-aarch64.patch

License: OpenSSL
URL: http://www.openssl.org/
BuildRequires: make
BuildRequires: gcc 
BuildRequires: coreutils, perl, sed, zlib-devel
BuildRequires: lksctp-tools-devel
# /usr/bin/cmp
BuildRequires: diffutils
# /usr/bin/rename
BuildRequires: util-linux


Requires: coreutils, make
Requires: %{name}-libs = %{version}-%{release}

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Requires: ca-certificates >= 2008-5
# Needed obsoletes due to the base/lib subpackage split
Obsoletes: openssl < 1.0.1b

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Requires: %{name}-libs = %{version}-%{release}
Requires: zlib-devel
Provides: openssl-devel

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Requires: %{name}-devel = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Requires: perl
Requires: %{name} = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q -n %{name}-%{version}/openssl

# The hobble_openssl is called here redundantly, just to be sure.
# The tarball has already the sources removed.
sh %{SOURCE1} > /dev/null

cp %{SOURCE12} crypto/ec/
cp %{SOURCE13} test/

%patch -P 1 -p1 -b .build
%patch -P 2 -p1 -b .defaults
%patch -P 3 -p1 -b .no-html
%patch -P 4 -p1 -b .man-rename

%patch -P 31 -p1 -b .conf-paths
%patch -P 32 -p1 -b .version-add-engines
%patch -P 33 -p1 -b .dgst
%patch -P 36 -p1 -b .no-brainpool
%patch -P 37 -p1 -b .curves
%patch -P 38 -p1 -b .no-weak-verify
%patch -P 40 -p1 -b .disable-ssl3
%patch -P 41 -p1 -b .system-cipherlist
%patch -P 42 -p1 -b .fips
%patch -P 44 -p1 -b .version-override
%patch -P 45 -p1 -b .weak-ciphers
%patch -P 46 -p1 -b .seclevel
%patch -P 47 -p1 -b .ts-sha256-default
%patch -P 48 -p1 -b .fips-post-rand
%patch -P 49 -p1 -b .evp-kdf
%patch -P 50 -p1 -b .ssh-kdf
%patch -P 51 -p1 -b .intel-cet
%patch -P 52 -p1 -b .s390x-update
%patch -P 53 -p1 -b .crng-test
%patch -P 55 -p1 -b .arm-update
%patch -P 56 -p1 -b .s390x-ecc
%patch -P 57 -p1 -b .opt-rsa
%patch -P 58 -p1 -b .opt-aes-gcm
%patch -P 59 -p1 -b .opt-aem-xts
%patch -P 60 -p1 -b .krb5-kdf
%patch -P 61 -p1 -b .edk2-build
%patch -P 62 -p1 -b .fips-curves
%patch -P 65 -p1 -b .drbg-selftest
%patch -P 66 -p1 -b .fips-dh
%patch -P 67 -p1 -b .kdf-selftest
%patch -P 69 -p1 -b .alpn-cb
%patch -P 70 -p1 -b .rewire-fips-drbg

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch x86_64
sslflags=enable-ec_nistp_64_gcc_128
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
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch aarch64
sslarch=linux-aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch mips mipsel
sslarch="linux-mips32 -mips32r2"
%endif
%ifarch mips64 mips64el
sslarch="linux64-mips64 -mips64r2"
%endif
%ifarch mips64el
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch riscv64
sslarch=linux-generic64
%endif

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS"

export HASHBANGPERL=/usr/bin/perl

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
export CFLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64"
export CPPFLAGS="$CPPFLAGS -D_FILE_OFFSET_BITS=64"
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	zlib enable-camellia enable-seed enable-rfc3779 \
	enable-cms enable-md2 enable-rc5 enable-ssl3 enable-ssl3-method \
	enable-weak-ssl-ciphers \
	no-mdc2 no-ec2m no-sm2 no-sm4 \
	shared  ${sslarch} %{?!nofips:fips} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""'

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

%make_build

# Overwrite FIPS README
cp -f %{SOURCE11} .

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check


%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}
# We don't need to install docs now because we don't package it.
%{__make} DESTDIR=%{?buildroot} INSTALL="%{__install} -p" install_sw install_ssldirs
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	
	chmod 755 ${lib}
	
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
	
done
# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
#install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_docdir}/Makefile.certificate - docs aren't build
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/make-dummy-cert
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_bindir}/renew-dummy-cert

# docs are disabled
# BEGIN
# Rename man pages so that they don't conflict with other system man pages.
#pushd $RPM_BUILD_ROOT %%{_mandir}
#ln -s -f config.5 man5/openssl.cnf.5
#for manpage in man*/* ; do
#	if [ -L ${manpage} ]; then
#		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
#		ln -snf ${TARGET}ssl ${manpage}ssl
#		rm -f ${manpage}
#	else
#		mv ${manpage} ${manpage}ssl
#	fi
#done
#for conflict in passwd rand ; do
#	rename ${conflict} ssl${conflict} man*/${conflict}*
# Fix dangling symlinks
#	manpage=man1/openssl-${conflict}.*
#	if [ -L ${manpage} ] ; then
#		ln -snf ssl${conflict}.1ssl ${manpage}
#	fi
#done
#popd
# END

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the config file timestamps are identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/ct_log_list.cnf

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/ct_log_list.cnf.dist

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

# Next step of gradual disablement of SSL3.
# Make SSL3 disappear to newly built dependencies.
sed -i '/^\#ifndef OPENSSL_NO_SSL_TRACE/i\
#ifndef OPENSSL_NO_SSL3\
# define OPENSSL_NO_SSL3\
#endif' $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h

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
LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH

%files
%{_bindir}/c_rehash
%license LICENSE
%doc FAQ NEWS README README.FIPS
%{_bindir}/make-dummy-cert
%{_bindir}/renew-dummy-cert
%{_bindir}/openssl
# docs are disabled
# BEGIN
#%%{_mandir}/man1*/*
#%%{_mandir}/man5*/*
#%%{_mandir}/man7*/*
#%%{_docdir}/Makefile.certificate
#%exclude %%{_mandir}/man1*/*.pl*
#%exclude %%{_mandir}/man1*/c_rehash*
#%exclude %%{_mandir}/man1*/tsget*
#%exclude %%{_mandir}/man1*/openssl-tsget*
# END
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config %{_sysconfdir}/pki/tls/openssl.cnf
%config %{_sysconfdir}/pki/tls/ct_log_list.cnf

%files libs
%license LICENSE
%{_libdir}/libcrypto.so.%{version}
%{_libdir}/libssl.so.%{version}
%{_libdir}/libcrypto.so.%{soversion}
%{_libdir}/libssl.so.%{soversion}

#%attr(0644,root,root) %%{_libdir}/.libcrypto.so.*.hmac
#%attr(0644,root,root) %%{_libdir}/.libssl.so.*.hmac
%{_libdir}/engines-%{soversion}

%files devel
%doc CHANGES doc/dir-locals.example.el doc/openssl-c-indent.el
%{_prefix}/include/openssl
%{_libdir}/*.so
#%%{_mandir}/man3*/*  docs are disabled
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a

%files perl
%{_bindir}/c_rehash
%{_sysconfdir}/pki/tls/misc/*.pl
%{_sysconfdir}/pki/tls/misc/tsget
# docs are disabled
# BEGIN
#%%{_mandir}/man1*/*.pl*
#%%{_mandir}/man1*/c_rehash*
#%%{_mandir}/man1*/tsget*
#%%{_mandir}/man1*/openssl-tsget*
# END
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

