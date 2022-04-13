<script>
	window.history.go(-1);
</script>
<?php
error_reporting(E_ALL || ~E_NOTICE);
show_source(__FILE__);
$name=$_POST['name'];
$age=$_POST['age'];
$height=$_POST['height'];
$weight=$_POST['weight'];
class Guest{
	public $name;
	public $information;
	public function __construct($name,$information)
	{
		$this->name=$name;
		$this->information=$information;
	}
	public function __wakeup()
	{
		$this->information->confirm();	
	}

}

class information{
	public $age;
	public $height;
	public $weight;
	public function __construct($age,$height,$weight)
	{
		$this->age=$age;
		$this->height=$height;
		$this->weight=$weight;
	}
	public function confirm()
	{
		echo "今天偷个懒吧，这里的数据合法性就不校验了.<br>";
		
	}
}

class Admin{
	public $admin;
	public function work(){
		include("admin.php");
	}
	
	public function __call($method,$args){
		echo "发生甚么事了？<br>";
		echo "current admin is $this->admin<br>";
		$this->work();
	}
		
	public function __toString()
	{
		echo "something error,use shell to debug!<br>";
		$shellcode=$_GET['shell'];
		if($_SERVER["REMOTE_ADDR"]!="127.0.0.1"){
			echo "limited shell<br>";
			if(isset($shellcode))
			{
				if(preg_match('/data:\/\/|filter:\/\/|php:\/\//i',$shellcode))
					die("hacker!");
				if(preg_replace('/[a-z,_]+\((?R)?\)/', NULL, $shellcode)!==';')
					die("no!no!no!");
				if(preg_match('/current|show_source/i',$shellcode))
					die("clever hacker!");
				eval($shellcode);
			}
		}else eval($shellcode);
	}	
}
if(isset($name)&&isset($age)&&isset($height)&&isset($weight))
	{
		$r=serialize(new information($age,$height,$weight));
		$t=serialize(new Guest($name,new information($age,$height,$weight)));
	}

$ban='/flag/i';
$t=preg_replace($ban, 'xdl', $t);//想读flag？想多了！
unserialize($t);
?>
