#coding:utf-8
#TODO: Change config file to json
#TODO: Automatic config init

config = {
	"VERSION":"2.6.1-alpha",
	"WEB_API_VERSION":"0.5.1_pre_alpha",
	"localAddress":"127.0.0.1",
	"localPort":1087,
	"excludeRemarks":[
		"剩余流量",
		"到期时间",
		"过期时间"
	],
	"web":{
		"listen":"127.0.0.1",
		"port":10870,
		"token":""
	},
	"exportResult":{
		"hideMaxSpeed":True,
		"uploadResult":False,
		"font":"./resources/fonts/SourceHanSansCN-Medium.otf",
		"colors":[
			{
				"name":"origin",
				"colors":{
					"0.064":[128,255,0],
					"0.512":[255,255,0],
					"4.0":[255,128,192],
					"16.0":[255,0,0]
				}
			},
			{
				"name":"chunxiaoyi",
				"colors":{
					"0.064":[102,255,102],
					"0.512":[255,255,102],
					"4.0":[255,178,102],
					"16.0":[255,102,102],
					"24.0":[226,140,255],
					"32.0":[102,204,255],
					"40.0":[102,102,255]
				}
			}
		]
	},
	"uploadResult":{
		"apiToken":"",
		"server":"",
		"remark":"Example Remark."
	},
	"downloadRules":{
		"maxThread":4,	#Thread count
		"buffer":4096,	#Buffer size,bytes
		"skipRuleMatch": False,
		"rules":[
			{
				"mode":"match_isp", #match_isp or match_location
				"ISP":"Microsoft Corporation",
				"tag":"Google"
			},
			{
				"mode":"match_isp",
				"ISP":"Google LLC",
				"tag":"Default"
			}
		],
		"downloadLinks":[
			{
				"link":"https://download.microsoft.com/download/0/A/F/0AFB5316-3062-494A-AB78-7FB0D4461357/7601.17514.101119-1850_Update_Sp_Wave1-GRMSP1.1_DVD.iso",
				"fileSize":1900,	#File size,MBytes
				"tag":"Default"
			},
			{
				"link":"https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe",
				"fileSize":971,	#File size,MBytes
				"tag":"Google"
			}
		]
	},
	"webPageSimulation":{
		"maxThread": 4,
		"urls":[
			"https://www.google.com.hk",
			"https://www.youtube.com",
			"https://www.bing.com",
			"https://www.github.com",
			"https://www.microsoft.com"
		],
		"cnUrls":[
			"https://www.baidu.com",
			"https://www.weibo.com",
			"https://www.qq.com"
		]
	}
}

config["speedTestDownload"] = config["downloadRules"] #TODO: Deprecate

