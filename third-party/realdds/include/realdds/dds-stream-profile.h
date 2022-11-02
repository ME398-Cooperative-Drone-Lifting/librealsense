// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2022 Intel Corporation. All Rights Reserved.

#pragma once


#include <third-party/json_fwd.hpp>

#include <stdint.h>
#include <string>
#include <vector>
#include <memory>


namespace realdds {


// Similar to fourcc, this describes how a stream data is organized. The characters are zero-terminated so it can be
// shorter than 'size' and can be easily converted from/to string.
//
struct dds_stream_format
{
    static constexpr size_t size = 4;
    char data[size+1];  // add a terminating NULL for ease

    dds_stream_format()
        : data{ 0 }
    {
    }

    dds_stream_format( std::string const & s );
    dds_stream_format( dds_stream_format const & ) = default;
    dds_stream_format( dds_stream_format && ) = default;

    bool is_valid() const { return data[0] != 0; }
    operator bool() const { return is_valid(); }

    std::string to_string() const { return std::string( data ); }
    operator std::string() const { return to_string(); }

    static dds_stream_format from_rs2( int rs2_format );
    int to_rs2() const;
};


class dds_stream_base;


class dds_stream_profile
{
    dds_stream_format _format;
    int16_t _frequency;  // "Frames" per second

    std::weak_ptr< dds_stream_base > _stream;

public:
    virtual ~dds_stream_profile() {}

protected:
    dds_stream_profile( dds_stream_format format, int16_t frequency )
        : _format( format )
        , _frequency( frequency )
    {
    }
    dds_stream_profile( dds_stream_profile && ) = default;

public:
    std::shared_ptr< dds_stream_base > stream() const { return _stream.lock(); }
    // This is for initialization and is called from dds_stream_base only!
    void init_stream( std::weak_ptr< dds_stream_base > const & stream );

    dds_stream_format format() const { return _format; }
    int16_t frequency() const { return _frequency; }

    // These are for debugging - not functional
    virtual std::string to_string() const;
    virtual std::string details_to_string() const;

    // Serialization to a JSON representation
    virtual nlohmann::json to_json() const;
};


typedef std::vector< std::shared_ptr< dds_stream_profile > > dds_stream_profiles;


class dds_video_stream_profile : public dds_stream_profile
{
    typedef dds_stream_profile super;

    uint16_t _width;   // Resolution width [pixels]
    uint16_t _height;  // Resolution height [pixels]

public:
    dds_video_stream_profile( dds_stream_format format, int16_t frequency, uint16_t width, uint16_t height )
        : super( format, frequency )
        , _width( width )
        , _height( height )
    {
    }
    dds_video_stream_profile( dds_video_stream_profile && ) = default;

    uint16_t width() const { return _width; }
    uint16_t height() const { return _height; }

    std::string details_to_string() const override;

    nlohmann::json to_json() const override;
};


class dds_motion_stream_profile : public dds_stream_profile
{
    typedef dds_stream_profile super;

public:
    dds_motion_stream_profile( dds_stream_format format, int16_t frequency )
        : super( format, frequency )
    {
    }
    dds_motion_stream_profile( dds_motion_stream_profile && ) = default;
};


}  // namespace realdds
